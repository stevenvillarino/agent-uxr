"""
Cerebras User Research Automation Example
Based on: https://inference-docs.cerebras.ai/cookbook/agents/automate-user-research

This is a direct implementation of the Cerebras approach for comparison with our enhanced system.
"""

import os
import time
from typing import Dict, List, TypedDict
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configuration
DEFAULT_NUM_INTERVIEWS = 5  # Reduced for faster testing
DEFAULT_NUM_QUESTIONS = 5

#==============================================================================
# DATA MODELS (matching Cerebras approach)
#==============================================================================

class Persona(BaseModel):
    """User persona for synthetic interviews"""
    name: str = Field(..., description="Full name of the persona")
    age: int = Field(..., description="Age in years")
    job: str = Field(..., description="Job title or role")
    traits: List[str] = Field(..., description="3-4 personality traits")
    communication_style: str = Field(..., description="How this person communicates")
    background: str = Field(..., description="One background detail shaping their perspective")

class PersonasList(BaseModel):
    """List of personas"""
    personas: List[Persona] = Field(..., description="List of generated personas")

class Questions(BaseModel):
    """List of interview questions"""
    questions: List[str] = Field(..., description="List of interview questions")

class InterviewState(TypedDict):
    """State shared across all nodes in the workflow"""
    # Configuration inputs
    research_question: str
    target_demographic: str
    num_interviews: int
    num_questions: int
    
    # Generated data
    interview_questions: List[str]
    personas: List[Persona]
    
    # Current interview tracking
    current_persona_index: int
    current_question_index: int
    current_interview_history: List[Dict]
    
    # Results storage
    all_interviews: List[Dict]
    synthesis: str

#==============================================================================
# LLM SETUP
#==============================================================================

def get_llm():
    """
    Get LLM instance - uses Claude instead of Cerebras for better availability
    You can swap this for Cerebras if you have an API key
    """
    try:
        # Try Anthropic first (better for research)
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=800
        )
    except:
        # Fallback to OpenAI
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=800
        )

def ask_ai(prompt: str) -> str:
    """Send prompt to AI and return response"""
    llm = get_llm()
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content if hasattr(response, 'content') else str(response)

#==============================================================================
# NODE FUNCTIONS (matching Cerebras structure)
#==============================================================================

def configuration_node(state: InterviewState) -> Dict:
    """Get user inputs and generate interview questions"""
    print(f"\n🔧 Configuring research: {state['research_question']}")
    print(f"📊 Planning {state['num_interviews']} interviews with {state['num_questions']} questions each")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(Questions)
    
    question_gen_prompt = f"""Generate exactly {state['num_questions']} interview questions about: {state['research_question']}

Requirements:
- Each question must be open-ended (not yes/no)
- Keep questions conversational and clear
- One question per line
- No numbering, bullets, or extra formatting

Target demographic: {state['target_demographic']}"""

    try:
        questions_result = structured_llm.invoke([{"role": "user", "content": question_gen_prompt}])
        questions = questions_result.questions if isinstance(questions_result, Questions) else []
        
        if not questions:
            questions = [
                f"How do you currently approach {state['research_question']}?",
                "What challenges do you face?",
                "What would make your experience better?",
                "How does this compare to alternatives?",
                "What's most important to you?"
            ]
        
        print(f"✅ Generated {len(questions)} questions")
        
        return {
            "num_questions": len(questions),
            "num_interviews": state['num_interviews'],
            "interview_questions": questions
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"interview_questions": [], "num_questions": 0, "num_interviews": 0}

def persona_generation_node(state: InterviewState) -> Dict:
    """Generate diverse personas for interviews"""
    num_personas = state['num_interviews']
    demographic = state['target_demographic']
    
    print(f"\n👥 Creating {num_personas} personas...")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(PersonasList)
    
    persona_prompt = f"""Generate exactly {num_personas} unique personas for an interview.
Each should belong to the target demographic: {demographic}.

Requirements:
- Realistic and diverse
- Different backgrounds and perspectives
- Believable personality traits
- Varied communication styles

Return as JSON matching the PersonasList schema."""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            personas_result = structured_llm.invoke([{"role": "user", "content": persona_prompt}])
            
            if isinstance(personas_result, PersonasList):
                personas = personas_result.personas
            else:
                raise ValueError("Invalid persona format")
            
            if len(personas) != num_personas:
                print(f"⚠️  Expected {num_personas} personas, got {len(personas)}")
            
            print(f"✅ Created {len(personas)} personas:")
            for i, p in enumerate(personas, 1):
                print(f"  {i}. {p.name} ({p.age}, {p.job})")
            
            return {
                "personas": personas,
                "current_persona_index": 0,
                "current_question_index": 0,
                "all_interviews": []
            }
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                print("Using fallback personas...")
                return {
                    "personas": [],
                    "current_persona_index": 0,
                    "current_question_index": 0,
                    "all_interviews": []
                }

def interview_node(state: InterviewState) -> Dict:
    """Conduct interview with current persona"""
    if not state.get('personas'):
        return {
            "current_persona_index": state.get('current_persona_index', 0) + 1
        }
    
    persona = state['personas'][state['current_persona_index']]
    question = state['interview_questions'][state['current_question_index']]
    
    print(f"\n💬 Interview {state['current_persona_index'] + 1}/{len(state['personas'])} - {persona.name}")
    print(f"Q{state['current_question_index'] + 1}: {question}")
    
    # Generate response as this persona with detailed character context
    interview_prompt = f"""You are {persona.name}, a {persona.age}-year-old {persona.job} who is {', '.join(persona.traits)}.
Your communication style: {persona.communication_style}
Your background: {persona.background}

Answer the following question in 2-3 sentences:

Question: {question}

Answer as {persona.name} in your own authentic voice. Be brief but creative and unique, and make each answer conversational.
BE REALISTIC – do not be overly optimistic. Mimic real human behavior based on your persona, and give honest answers."""

    try:
        answer = ask_ai(interview_prompt)
        print(f"A: {answer}")
        
        # Update state with interview history
        history = state.get('current_interview_history', []) + [{
            "question": question,
            "answer": answer
        }]
        
        # Check if this interview is complete
        if state['current_question_index'] + 1 >= len(state['interview_questions']):
            # Interview complete - save it and move to next persona
            print(f"✓ Completed interview with {persona.name}")
            return {
                "all_interviews": state['all_interviews'] + [{
                    'persona': persona,
                    'responses': history
                }],
                "current_interview_history": [],
                "current_question_index": 0,
                "current_persona_index": state['current_persona_index'] + 1
            }
        
        # Continue with next question for same persona
        return {
            "current_interview_history": history,
            "current_question_index": state['current_question_index'] + 1
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "current_persona_index": state['current_persona_index'] + 1
        }

def synthesis_node(state: InterviewState) -> Dict:
    """Synthesize insights from all interviews"""
    print("\n🧠 Analyzing all interviews...")
    
    # Compile all responses
    interview_summary = f"Research Question: {state['research_question']}\n"
    interview_summary += f"Target Demographic: {state['target_demographic']}\n"
    interview_summary += f"Number of Interviews: {len(state['all_interviews'])}\n\n"
    
    for i, interview in enumerate(state['all_interviews'], 1):
        p = interview['persona']
        interview_summary += f"Interview {i} - {p.name} ({p.age}, {p.job}):\n"
        interview_summary += f"Persona Traits: {', '.join(p.traits)}\n"
        for j, qa in enumerate(interview['responses'], 1):
            interview_summary += f"Q{j}: {qa['question']}\n"
            interview_summary += f"A{j}: {qa['answer']}\n"
        interview_summary += "\n"
    
    synthesis_prompt = f"""Analyze these {len(state['all_interviews'])} user interviews about "{state['research_question']}" among {state['target_demographic']} and provide a concise yet comprehensive analysis:

1. KEY THEMES: What patterns and common themes emerged across all interviews?
2. DIVERSE PERSPECTIVES: What different viewpoints or unique insights did different personas provide?
3. PAIN POINTS & OPPORTUNITIES: What challenges, frustrations, or unmet needs were identified?
4. ACTIONABLE RECOMMENDATIONS: Based on these insights, what specific actions should be taken?

Interview Data:
{interview_summary}"""

    try:
        synthesis = ask_ai(synthesis_prompt)
        
        print("\n" + "="*60)
        print("🎯 COMPREHENSIVE RESEARCH INSIGHTS")
        print("="*60)
        print(f"Research Topic: {state['research_question']}")
        print(f"Demographic: {state['target_demographic']}")
        print(f"Interviews Conducted: {len(state['all_interviews'])}")
        print("-"*60)
        print(synthesis)
        print("="*60)
        
        return {"synthesis": synthesis}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"synthesis": "Error generating synthesis"}

#==============================================================================
# ROUTER
#==============================================================================

def interview_router(state: InterviewState) -> str:
    """Route between continuing interviews or ending"""
    if not state.get('personas'):
        return "synthesize"
    
    if state['current_persona_index'] >= len(state['personas']):
        return "synthesize"
    else:
        return "interview"

#==============================================================================
# WORKFLOW BUILDER
#==============================================================================

def build_interview_workflow():
    """Build the complete interview workflow graph"""
    workflow = StateGraph(InterviewState)
    
    # Add all our specialized nodes
    workflow.add_node("config", configuration_node)
    workflow.add_node("personas", persona_generation_node)
    workflow.add_node("interview", interview_node)
    workflow.add_node("synthesize", synthesis_node)
    
    # Define the workflow connections
    workflow.set_entry_point("config")
    workflow.add_edge("config", "personas")
    workflow.add_edge("personas", "interview")
    
    # Conditional routing based on interview progress
    workflow.add_conditional_edges(
        "interview",
        interview_router,
        {
            "interview": "interview",    # Continue interviewing
            "synthesize": "synthesize"   # All done, analyze results
        }
    )
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

#==============================================================================
# MAIN EXECUTION
#==============================================================================

def run_research_system(research_question: str = None, target_demographic: str = None):
    """Execute the complete LangGraph research workflow"""
    
    # Get inputs if not provided
    if not research_question:
        research_question = input("\n📝 What research question would you like to explore? ")
    if not target_demographic:
        target_demographic = input("👥 What kinds of users would you like to interview? ")
    
    workflow = build_interview_workflow()
    
    start_time = time.time()
    
    # Initialize state
    initial_state = {
        "research_question": research_question,
        "target_demographic": target_demographic,
        "num_interviews": DEFAULT_NUM_INTERVIEWS,
        "num_questions": DEFAULT_NUM_QUESTIONS,
        "interview_questions": [],
        "personas": [],
        "current_persona_index": 0,
        "current_question_index": 0,
        "current_interview_history": [],
        "all_interviews": [],
        "synthesis": ""
    }
    
    try:
        print("\n" + "="*60)
        print("🚀 CEREBRAS-STYLE USER RESEARCH AUTOMATION")
        print("="*60)
        
        final_state = workflow.invoke(initial_state, {"recursion_limit": 100})
        
        total_time = time.time() - start_time
        print(f"\n✅ Workflow complete! {len(final_state['all_interviews'])} interviews in {total_time:.1f}s")
        
        return final_state
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        return None

#==============================================================================
# CLI
#==============================================================================

if __name__ == "__main__":
    print("\n🧪 Testing Cerebras User Research Automation Approach\n")
    
    # Example usage
    result = run_research_system(
        research_question="developer experience with AI coding assistants",
        target_demographic="professional software developers"
    )
    
    if result:
        print("\n📊 FINAL RESULTS:")
        print(f"- Personas interviewed: {len(result.get('all_interviews', []))}")
        print(f"- Questions asked: {len(result.get('interview_questions', []))}")
        print(f"- Synthesis length: {len(result.get('synthesis', ''))} characters")
