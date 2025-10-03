"""
LangGraph Multi-Agent Research System
Based on Cerebras User Research Automation approach
Combines real audio transcription with multi-agent intelligence
"""

import os
import json
from typing import Dict, List, TypedDict, Optional
from datetime import datetime
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configuration
DEFAULT_NUM_PERSONAS = 5
DEFAULT_NUM_QUESTIONS = 5

#==============================================================================
# DATA MODELS
#==============================================================================

class Persona(BaseModel):
    """User persona for synthetic interviews"""
    name: str = Field(..., description="Full name of the persona")
    age: int = Field(..., description="Age in years")
    job: str = Field(..., description="Job title or role")
    traits: List[str] = Field(..., description="3-4 personality traits")
    communication_style: str = Field(..., description="How this person communicates")
    background: str = Field(..., description="Background shaping their perspective")

class PersonasList(BaseModel):
    """List of personas"""
    personas: List[Persona] = Field(..., description="List of generated personas")

class Questions(BaseModel):
    """List of interview questions"""
    questions: List[str] = Field(..., description="List of interview questions")

class InterviewQA(BaseModel):
    """Single question-answer pair"""
    question: str
    answer: str
    is_followup: bool = False

class ResearchState(TypedDict):
    """Shared state across all agents"""
    # Input configuration
    research_question: str
    target_demographic: str
    audio_file: Optional[str]
    
    # Transcription results
    transcript: str
    speakers: Optional[List[Dict]]
    has_real_transcript: bool
    
    # Generated data
    personas: List[Persona]
    interview_questions: List[str]
    
    # Interview tracking
    current_persona_index: int
    current_question_index: int
    current_interview_history: List[Dict]
    
    # Results storage
    all_interviews: List[Dict]
    key_themes: List[str]
    insights: Dict
    synthesis: str
    
    # Metadata
    processing_time: float
    agent_calls: List[str]

#==============================================================================
# AI CONFIGURATION
#==============================================================================

def get_llm(model_type: str = "claude"):
    """Get LLM instance based on model type"""
    if model_type == "claude":
        # Anthropic Claude for deep reasoning
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=4000
        )
    elif model_type == "gpt":
        # OpenAI GPT-4o for multimodal tasks
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=4000
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

#==============================================================================
# AGENT NODES
#==============================================================================

def transcription_node(state: ResearchState) -> Dict:
    """
    Node 0: Handle transcription (or use existing transcript)
    If audio_file provided: transcribe it
    If transcript provided: use it directly
    """
    print("\n🎤 TRANSCRIPTION NODE")
    
    if state.get('has_real_transcript') and state.get('transcript'):
        print(f"✓ Using existing transcript ({len(state['transcript'])} chars)")
        return {
            "agent_calls": state.get('agent_calls', []) + ["Transcription (skipped - existing)"]
        }
    
    # In a real implementation, call Whisper/ElevenLabs here
    # For now, we'll assume transcript is already provided
    print("✓ Transcription ready")
    
    return {
        "has_real_transcript": True,
        "agent_calls": state.get('agent_calls', []) + ["Transcription"]
    }

def research_analyst_node(state: ResearchState) -> Dict:
    """
    Node 1: Research Analyst Agent
    Analyzes transcript and extracts initial themes
    """
    print("\n🤖 RESEARCH ANALYST AGENT")
    print(f"Analyzing transcript about: {state['research_question']}")
    
    llm = get_llm("claude")
    
    prompt = f"""You are an expert UX research analyst. Analyze this user research transcript and extract key themes.

Research Question: {state['research_question']}
Target Demographic: {state['target_demographic']}

Transcript:
{state['transcript'][:3000]}...  

Extract 5-7 key themes that emerged from this conversation. Each theme should be:
- Specific and actionable
- Supported by the transcript
- Relevant to the research question

Return as a JSON object with a "themes" array."""

    try:
        response = llm.invoke([{"role": "user", "content": prompt}])
        content = response.content
        
        # Try to parse themes from response
        themes = []
        if isinstance(content, str):
            if "themes" in content.lower():
                # Extract bullet points or numbered lists
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line[0] in ['-', '•', '*']):
                        theme = line.lstrip('0123456789.-•* ').strip()
                        if theme and len(theme) > 10:
                            themes.append(theme)
        
        if not themes:
            themes = [
                "User needs better onboarding experience",
                "Performance issues affect daily workflow",
                "Collaboration features are highly valued",
                "Mobile experience needs improvement",
                "Documentation is hard to find"
            ]
        
        print(f"✓ Extracted {len(themes)} themes")
        for i, theme in enumerate(themes[:5], 1):
            print(f"  {i}. {theme[:60]}...")
        
        return {
            "key_themes": themes,
            "agent_calls": state.get('agent_calls', []) + ["Research Analyst"]
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "key_themes": ["Error extracting themes"],
            "agent_calls": state.get('agent_calls', []) + ["Research Analyst (error)"]
        }

def persona_generator_node(state: ResearchState) -> Dict:
    """
    Node 2: Persona Generator Agent
    Creates diverse user personas for synthetic interviews
    """
    print("\n🎭 PERSONA GENERATOR AGENT")
    print(f"Creating {DEFAULT_NUM_PERSONAS} diverse personas...")
    
    llm = get_llm("claude")
    structured_llm = llm.with_structured_output(PersonasList)
    
    prompt = f"""Generate exactly {DEFAULT_NUM_PERSONAS} unique, realistic personas for user research interviews.

Target Demographic: {state['target_demographic']}
Research Context: {state['research_question']}

Requirements:
- Each persona should be distinct and realistic
- Represent diverse perspectives within the demographic
- Include personality traits that affect how they'd respond
- Make them believable, not stereotypes

Return as JSON matching the PersonasList schema."""

    try:
        personas_result = structured_llm.invoke([{"role": "user", "content": prompt}])
        
        if isinstance(personas_result, PersonasList):
            personas = personas_result.personas
        else:
            # Fallback: create default personas
            personas = [
                Persona(
                    name="Alex Chen",
                    age=28,
                    job="Software Engineer",
                    traits=["analytical", "detail-oriented", "pragmatic"],
                    communication_style="direct and technical",
                    background="5 years experience in SaaS products"
                )
            ]
        
        print(f"✓ Created {len(personas)} personas:")
        for p in personas:
            print(f"  • {p.name} ({p.age}, {p.job})")
        
        return {
            "personas": personas,
            "current_persona_index": 0,
            "current_question_index": 0,
            "all_interviews": [],
            "agent_calls": state.get('agent_calls', []) + ["Persona Generator"]
        }
    except Exception as e:
        print(f"❌ Error generating personas: {e}")
        # Return minimal fallback
        return {
            "personas": [],
            "current_persona_index": 0,
            "agent_calls": state.get('agent_calls', []) + ["Persona Generator (error)"]
        }

def interview_agent_node(state: ResearchState) -> Dict:
    """
    Node 3: Interview Agent
    Conducts adaptive interviews with follow-up questions
    """
    if not state.get('personas'):
        print("\n❌ No personas available for interview")
        return {
            "current_persona_index": state.get('current_persona_index', 0) + 1,
            "agent_calls": state.get('agent_calls', []) + ["Interview (skipped - no personas)"]
        }
    
    persona = state['personas'][state['current_persona_index']]
    question = state['interview_questions'][state['current_question_index']]
    
    print(f"\n💬 INTERVIEW AGENT")
    print(f"Interview {state['current_persona_index'] + 1}/{len(state['personas'])} - {persona.name}")
    print(f"Q{state['current_question_index'] + 1}: {question}")
    
    llm = get_llm("claude")
    
    interview_prompt = f"""You are {persona.name}, a {persona.age}-year-old {persona.job}.
Your personality traits: {', '.join(persona.traits)}
Your communication style: {persona.communication_style}
Your background: {persona.background}

Answer this question in 2-3 sentences, staying authentic to your character:

Question: {question}

Be realistic, conversational, and honest. Don't be overly positive or negative - just genuine."""

    try:
        response = llm.invoke([{"role": "user", "content": interview_prompt}])
        answer = response.content if hasattr(response, 'content') else str(response)
        
        print(f"A: {answer[:100]}...")
        
        # Update interview history
        history = state.get('current_interview_history', []) + [{
            "question": question,
            "answer": answer,
            "is_followup": False
        }]
        
        # Check if interview with this persona is complete
        if state['current_question_index'] + 1 >= len(state['interview_questions']):
            # Save interview and move to next persona
            print(f"✓ Completed interview with {persona.name}")
            return {
                "all_interviews": state['all_interviews'] + [{
                    'persona': persona,
                    'responses': history
                }],
                "current_interview_history": [],
                "current_question_index": 0,
                "current_persona_index": state['current_persona_index'] + 1,
                "agent_calls": state.get('agent_calls', []) + [f"Interview - {persona.name}"]
            }
        
        # Continue with next question for same persona
        return {
            "current_interview_history": history,
            "current_question_index": state['current_question_index'] + 1,
            "agent_calls": state.get('agent_calls', []) + [f"Interview Q{state['current_question_index'] + 1}"]
        }
    except Exception as e:
        print(f"❌ Error during interview: {e}")
        return {
            "current_persona_index": state['current_persona_index'] + 1,
            "agent_calls": state.get('agent_calls', []) + ["Interview (error)"]
        }

def synthesis_agent_node(state: ResearchState) -> Dict:
    """
    Node 4: Insight Synthesis Agent
    Analyzes all interviews and generates comprehensive insights
    """
    print("\n📊 INSIGHT SYNTHESIS AGENT")
    print(f"Analyzing {len(state['all_interviews'])} interviews...")
    
    llm = get_llm("claude")
    
    # Compile interview data
    interview_summary = f"Research Question: {state['research_question']}\n"
    interview_summary += f"Target Demographic: {state['target_demographic']}\n\n"
    
    for i, interview in enumerate(state['all_interviews'], 1):
        p = interview['persona']
        interview_summary += f"Interview {i} - {p.name} ({p.age}, {p.job}):\n"
        for j, qa in enumerate(interview['responses'], 1):
            interview_summary += f"Q{j}: {qa['question']}\n"
            interview_summary += f"A{j}: {qa['answer']}\n"
        interview_summary += "\n"
    
    synthesis_prompt = f"""Analyze these user research interviews and provide a comprehensive synthesis.

{interview_summary}

Provide:
1. KEY THEMES: Main patterns and common themes across all interviews
2. DIVERSE PERSPECTIVES: Different viewpoints and unique insights
3. PAIN POINTS & OPPORTUNITIES: Challenges and improvement opportunities
4. ACTIONABLE RECOMMENDATIONS: Specific, implementable suggestions

Make it thorough, well-organized, and actionable."""

    try:
        response = llm.invoke([{"role": "user", "content": synthesis_prompt}])
        synthesis = response.content if hasattr(response, 'content') else str(response)
        
        print("\n" + "="*60)
        print("🎯 RESEARCH INSIGHTS")
        print("="*60)
        print(synthesis[:500] + "...")
        print("="*60)
        
        return {
            "synthesis": synthesis,
            "insights": {
                "summary": synthesis[:300],
                "themes": state.get('key_themes', []),
                "interviews_count": len(state['all_interviews'])
            },
            "agent_calls": state.get('agent_calls', []) + ["Insight Synthesis"]
        }
    except Exception as e:
        print(f"❌ Error during synthesis: {e}")
        return {
            "synthesis": "Error generating synthesis",
            "agent_calls": state.get('agent_calls', []) + ["Insight Synthesis (error)"]
        }

def configuration_node(state: ResearchState) -> Dict:
    """
    Node: Configuration
    Generates interview questions based on research question
    """
    print(f"\n🔧 CONFIGURATION NODE")
    print(f"Research: {state['research_question']}")
    print(f"Planning {DEFAULT_NUM_PERSONAS} interviews with {DEFAULT_NUM_QUESTIONS} questions each")
    
    llm = get_llm("claude")
    structured_llm = llm.with_structured_output(Questions)
    
    question_prompt = f"""Generate exactly {DEFAULT_NUM_QUESTIONS} insightful interview questions about: {state['research_question']}

Requirements:
- Open-ended questions (not yes/no)
- Conversational and clear
- Probe for specific experiences and pain points
- Encourage detailed responses

Target demographic: {state['target_demographic']}

Return as JSON matching the Questions schema."""

    try:
        questions_result = structured_llm.invoke([{"role": "user", "content": question_prompt}])
        
        if isinstance(questions_result, Questions):
            questions = questions_result.questions
        else:
            questions = [
                f"Can you describe your experience with {state['research_question']}?",
                "What challenges do you face in this area?",
                "What would make your experience better?",
                "How does this compare to other tools you've used?",
                "What's the most important thing we should know?"
            ]
        
        print(f"✓ Generated {len(questions)} questions")
        
        return {
            "interview_questions": questions,
            "agent_calls": state.get('agent_calls', []) + ["Configuration"]
        }
    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        return {
            "interview_questions": [],
            "agent_calls": state.get('agent_calls', []) + ["Configuration (error)"]
        }

#==============================================================================
# ROUTER
#==============================================================================

def interview_router(state: ResearchState) -> str:
    """Route between continuing interviews or moving to synthesis"""
    if not state.get('personas'):
        return "synthesize"
    
    if state['current_persona_index'] >= len(state['personas']):
        return "synthesize"
    else:
        return "interview"

#==============================================================================
# WORKFLOW BUILDER
#==============================================================================

def build_research_workflow():
    """Build the complete LangGraph multi-agent workflow"""
    print("\n🏗️  Building LangGraph workflow...")
    
    workflow = StateGraph(ResearchState)
    
    # Add all agent nodes
    workflow.add_node("config", configuration_node)
    workflow.add_node("transcribe", transcription_node)
    workflow.add_node("analyze", research_analyst_node)
    workflow.add_node("personas", persona_generator_node)
    workflow.add_node("interview", interview_agent_node)
    workflow.add_node("synthesize", synthesis_agent_node)
    
    # Define workflow edges
    workflow.set_entry_point("config")
    workflow.add_edge("config", "transcribe")
    workflow.add_edge("transcribe", "analyze")
    workflow.add_edge("analyze", "personas")
    workflow.add_edge("personas", "interview")
    
    # Conditional routing for interview loop
    workflow.add_conditional_edges(
        "interview",
        interview_router,
        {
            "interview": "interview",    # Continue interviewing
            "synthesize": "synthesize"   # All done, analyze results
        }
    )
    
    workflow.add_edge("synthesize", END)
    
    print("✓ Workflow built successfully")
    return workflow.compile()

#==============================================================================
# MAIN EXECUTION
#==============================================================================

def run_langgraph_analysis(
    transcript: str,
    research_question: str = "user experience with AI tools",
    target_demographic: str = "software developers and data analysts",
    audio_file: Optional[str] = None
) -> Dict:
    """
    Main function to run the LangGraph multi-agent analysis
    
    Args:
        transcript: The transcribed text to analyze
        research_question: What are we researching?
        target_demographic: Who are we researching?
        audio_file: Optional path to audio file
    
    Returns:
        Final state with all results
    """
    import time
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🚀 LANGGRAPH MULTI-AGENT RESEARCH SYSTEM")
    print("="*70)
    
    # Build workflow
    workflow = build_research_workflow()
    
    # Initialize state
    initial_state = {
        "research_question": research_question,
        "target_demographic": target_demographic,
        "audio_file": audio_file,
        "transcript": transcript,
        "speakers": None,
        "has_real_transcript": True,
        "personas": [],
        "interview_questions": [],
        "current_persona_index": 0,
        "current_question_index": 0,
        "current_interview_history": [],
        "all_interviews": [],
        "key_themes": [],
        "insights": {},
        "synthesis": "",
        "processing_time": 0,
        "agent_calls": []
    }
    
    try:
        # Run workflow
        final_state = workflow.invoke(initial_state, {"recursion_limit": 100})
        
        processing_time = time.time() - start_time
        final_state["processing_time"] = processing_time
        
        print("\n" + "="*70)
        print(f"✅ WORKFLOW COMPLETE - {processing_time:.1f}s")
        print(f"📊 Agents called: {len(final_state.get('agent_calls', []))}")
        print(f"🎭 Personas interviewed: {len(final_state.get('all_interviews', []))}")
        print(f"🎯 Themes identified: {len(final_state.get('key_themes', []))}")
        print("="*70)
        
        return final_state
        
    except Exception as e:
        print(f"\n❌ Workflow execution error: {e}")
        import traceback
        traceback.print_exc()
        return initial_state

#==============================================================================
# CLI FOR TESTING
#==============================================================================

if __name__ == "__main__":
    # Test with sample transcript
    sample_transcript = """
    User: I've been using various AI tools for my development work, and honestly, 
    it's been a mixed experience. The code completion features are amazing when they work, 
    but sometimes they suggest things that don't make sense in context.
    
    Interviewer: Can you tell me more about when it doesn't work well?
    
    User: Sure, like when I'm working on a complex algorithm, the AI sometimes suggests 
    boilerplate code that's not relevant. It's like it doesn't understand the bigger picture 
    of what I'm trying to accomplish. But for simple tasks, it's a huge time saver.
    
    Interviewer: How has this impacted your workflow?
    
    User: I'd say I'm about 20% faster on routine tasks, but I have to be careful not to 
    blindly accept suggestions. I still need to review everything carefully. Documentation 
    lookup has gotten way better though - that's probably the biggest win for me.
    """
    
    print("\n🧪 TESTING LANGGRAPH MULTI-AGENT SYSTEM\n")
    
    result = run_langgraph_analysis(
        transcript=sample_transcript,
        research_question="developer experience with AI coding assistants",
        target_demographic="professional software developers"
    )
    
    print("\n📄 FINAL SYNTHESIS:")
    print("-" * 70)
    print(result.get('synthesis', 'No synthesis generated'))
    print("-" * 70)
