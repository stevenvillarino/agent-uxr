"""
Cerebras User Research Automation Example
Based on: https://inference-docs.cerebras.ai/cookbook/agents/automate-user-research

This is the original Cerebras approach using LangGraph and Cerebras Llama 3.3 70B
"""

import logging
import sys
from typing import Dict, List, TypedDict
import time
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Configuration Constants
DEFAULT_NUM_INTERVIEWS = 10
DEFAULT_NUM_QUESTIONS = 5

#==============================================================================
# STEP 1: Setup LLM
#==============================================================================

def setup_llm():
    """
    Set up the LLM - you can choose between:
    1. Cerebras (original - requires CEREBRAS_API_KEY)
    2. OpenAI (fallback - requires OPENAI_API_KEY)
    3. Anthropic (alternative - requires ANTHROPIC_API_KEY)
    """
    
    # Try Cerebras first (original approach)
    if os.getenv("CEREBRAS_API_KEY"):
        try:
            from langchain_cerebras import ChatCerebras
            print("🚀 Using Cerebras Llama 3.3 70B (original)")
            return ChatCerebras(
                model="llama3.3-70b",
                temperature=0.7,
                max_tokens=800
            )
        except ImportError:
            print("⚠️  langchain-cerebras not installed")
    
    # Fallback to OpenAI
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        print("🔄 Using OpenAI GPT-4o (fallback)")
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=800
        )
    
    # Fallback to Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        print("🔄 Using Anthropic Claude (fallback)")
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=800
        )
    
    raise ValueError("No API key found. Set CEREBRAS_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")

# Initialize LLM
llm = setup_llm()

# System prompt
system_prompt = """You are a helpful assistant. Provide a direct, clear response without showing your thinking process. Respond directly without using <think> tags or showing internal reasoning."""

def ask_ai(prompt: str) -> str:
    """Send prompt to AI and return response"""
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    return response.content

print("✅ Setup complete")

#==============================================================================
# STEP 2: Define Data Models
#==============================================================================

from pydantic import BaseModel, Field, ValidationError

class Persona(BaseModel):
    name: str = Field(..., description="Full name of the persona")
    age: int = Field(..., description="Age in years")
    job: str = Field(..., description="Job title or role")
    traits: List[str] = Field(..., description="3-4 personality traits")
    communication_style: str = Field(..., description="How this person communicates")
    background: str = Field(..., description="One background detail shaping their perspective")

class PersonasList(BaseModel):
    personas: List[Persona] = Field(..., description="List of generated personas")

class InterviewState(TypedDict):
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

print("✅ State management ready")

#==============================================================================
# STEP 3: Define Core Node Functions
#==============================================================================

from pydantic import BaseModel, Field

class Questions(BaseModel):
    questions: List = Field(..., description="List of interview questions")

# Configuration Node
question_gen_prompt = """Generate exactly {num_questions} interview questions about: {research_question}. Use the provided structured output to format the questions."""

def configuration_node(state: InterviewState) -> Dict:
    """Get user inputs and generate interview questions"""
    
    print(f"\n🔧 Configuring research: {state['research_question']}")
    print(f"📊 Planning {DEFAULT_NUM_INTERVIEWS} interviews with {DEFAULT_NUM_QUESTIONS} questions each")
    
    structured_llm = llm.with_structured_output(Questions)
    questions = structured_llm.invoke(question_gen_prompt.format(
        num_questions=DEFAULT_NUM_QUESTIONS,
        research_question=state['research_question']
    ))
    questions = questions.questions
    print(f"✅ Generated {len(questions)} questions")
    
    return {
        "num_questions": DEFAULT_NUM_QUESTIONS,
        "num_interviews": DEFAULT_NUM_INTERVIEWS,
        "interview_questions": questions
    }

# Persona Generation Node
persona_prompt = (
    "Generate exactly {num_personas} unique personas for an interview. "
    "Each should belong to the target demographic: {demographic}. "
    "Respond only in JSON using this format: {{ personas: [ ... ] }}"
)

def persona_generation_node(state: InterviewState) -> Dict:
    
    num_personas = state['num_interviews']
    demographic = state['target_demographic']
    max_retries = 5
    
    print(f"\n👥 Creating {state['num_interviews']} personas...")
    
    structured_llm = llm.with_structured_output(PersonasList)
    
    for attempt in range(max_retries):
        try:
            raw_output = structured_llm.invoke([{
                "role": "user",
                "content": persona_prompt.format(
                    num_personas=num_personas,
                    demographic=demographic
                )
            }])
            
            if raw_output is None:
                raise ValueError("LLM returned None")
            
            validated = PersonasList.model_validate(raw_output)
            
            if len(validated.personas) != num_personas:
                raise ValueError(f"Expected {num_personas} personas, got {len(validated.personas)}")
            
            personas = validated.personas
            for i, p in enumerate(personas):
                print(f"Persona {i+1}: {p.name} ({p.age}, {p.job})")
            
            return {
                "personas": personas,
                "current_persona_index": 0,
                "current_question_index": 0,
                "all_interviews": []
            }
        
        except (ValidationError, ValueError, TypeError) as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise RuntimeError(f"❗️Failed after {max_retries} attempts")

# Interview Node
interview_prompt = """You are {persona_name}, a {persona_age}-year-old {persona_job} who is {persona_traits}.
Answer the following question in 2-3 sentences:

Question: {question}

Answer as {persona_name} in your own authentic voice. Be brief but creative and unique, and make each answer conversational.
BE REALISTIC – do not be overly optimistic. Mimic real human behavior based on your persona, and give honest answers."""

def interview_node(state: InterviewState) -> Dict:
    """Conduct interview with current persona"""
    persona = state['personas'][state['current_persona_index']]
    question = state['interview_questions'][state['current_question_index']]
    
    print(f"\n💬 Interview {state['current_persona_index'] + 1}/{len(state['personas'])} - {persona.name}")
    print(f"Q{state['current_question_index'] + 1}: {question}")
    
    # Generate response as this persona with detailed character context
    prompt = interview_prompt.format(
        persona_name=persona.name,
        persona_age=persona.age,
        persona_job=persona.job,
        persona_traits=', '.join(persona.traits),
        question=question
    )
    answer = ask_ai(prompt)
    print(f"A: {answer}")
    
    # Update state with interview history
    history = state.get('current_interview_history', []) + [{
        "question": question,
        "answer": answer
    }]
    
    # Check if this interview is complete
    if state['current_question_index'] + 1 >= len(state['interview_questions']):
        # Interview complete - save it and move to next persona
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

# Synthesis Node
synthesis_prompt_template = """Analyze these {num_interviews} user interviews about "{research_question}" among {target_demographic} and provide a concise yet comprehensive analysis:

1. KEY THEMES: What patterns and common themes emerged across all interviews? Look for similarities in responses, shared concerns, and recurring topics.

2. DIVERSE PERSPECTIVES: What different viewpoints or unique insights did different personas provide? Highlight contrasting opinions or approaches.

3. PAIN POINTS & OPPORTUNITIES: What challenges, frustrations, or unmet needs were identified? What opportunities for improvement emerged?

4. ACTIONABLE RECOMMENDATIONS: Based on these insights, what specific actions should be taken? Provide concrete, implementable suggestions.

Keep the analysis thorough but well-organized and actionable.

Interview Data:
{interview_summary}
"""

def synthesis_node(state: InterviewState) -> Dict:
    """Synthesize insights from all interviews"""
    print("\n🧠 Analyzing all interviews...")
    
    # Compile all responses in a structured format
    interview_summary = f"Research Question: {state['research_question']}\n"
    interview_summary += f"Target Demographic: {state['target_demographic']}\n"
    interview_summary += f"Number of Interviews: {len(state['all_interviews'])}\n\n"
    
    for i, interview in enumerate(state['all_interviews'], 1):
        p = interview['persona']
        interview_summary += f"Interview {i} - {p.name} ({p.age}, {p.job}):\n"
        interview_summary += f"Persona Traits: {p.traits}\n"
        for j, qa in enumerate(interview['responses'], 1):
            interview_summary += f"Q{j}: {qa['question']}\n"
            interview_summary += f"A{j}: {qa['answer']}\n"
        interview_summary += "\n"
    
    prompt = synthesis_prompt_template.format(
        num_interviews=len(state['all_interviews']),
        research_question=state['research_question'],
        target_demographic=state['target_demographic'],
        interview_summary=interview_summary
    )
    
    try:
        synthesis = ask_ai(prompt)
    except Exception as e:
        synthesis = f"Error during synthesis: {e}\n\nRaw interview data available for manual analysis."
    
    # Display results with better formatting
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

print("✅ Core nodes ready")

#==============================================================================
# STEP 4: Interview Router
#==============================================================================

def interview_router(state: InterviewState) -> str:
    """Route between continuing interviews or ending"""
    if state['current_persona_index'] >= len(state['personas']):
        return "synthesize"
    else:
        return "interview"

print("✅ Router ready")

#==============================================================================
# STEP 5: Build LangGraph Workflow
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

print("✅ Workflow builder ready")

#==============================================================================
# STEP 6: Run the Complete System
#==============================================================================

def run_research_system(research_question: str = None, target_demographic: str = None):
    """Execute the complete LangGraph research workflow"""
    
    if not research_question:
        research_question = input("\nWhat research question would you like to explore? ")
    if not target_demographic:
        target_demographic = input("What kinds of users would you like to interview? ")
    
    workflow = build_interview_workflow()
    
    # Try to display workflow graph
    try:
        from IPython.display import Image, display
        display(Image(workflow.get_graph(xray=True).draw_mermaid_png()))
    except:
        print("(Workflow visualization requires IPython - skipping)")
    
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
        final_state = workflow.invoke(initial_state, {"recursion_limit": 100})
        total_time = time.time() - start_time
        print(f"\n✅ Workflow complete! {len(final_state['all_interviews'])} interviews in {total_time:.1f}s")
        return final_state
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        return None

print("✅ Complete LangGraph system ready")

#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 CEREBRAS USER RESEARCH AUTOMATION")
    print("Based on: https://inference-docs.cerebras.ai/cookbook/agents/automate-user-research")
    print("="*70)
    
    # You can pass questions directly or leave blank for interactive mode
    result = run_research_system(
        research_question="developer experience with AI coding assistants",
        target_demographic="professional software developers"
    )
    
    if result:
        print("\n📄 FINAL SYNTHESIS:")
        print("-" * 70)
        print(result.get('synthesis', 'No synthesis generated'))
        print("-" * 70)
