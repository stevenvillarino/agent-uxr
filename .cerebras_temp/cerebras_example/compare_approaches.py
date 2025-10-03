#!/usr/bin/env python3
"""
Quick comparison test between Cerebras approach and InsightDeck approach
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_cerebras():
    """Test the original Cerebras approach"""
    print("\n" + "="*70)
    print("🧪 TESTING CEREBRAS APPROACH")
    print("="*70)
    
    try:
        from cerebras_example.automate_user_research import run_research_system
        
        result = run_research_system(
            research_question="user experience with project management tools",
            target_demographic="remote team leaders"
        )
        
        return result
    except Exception as e:
        print(f"❌ Cerebras test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_insightdeck():
    """Test the InsightDeck enhanced approach"""
    print("\n" + "="*70)
    print("🧪 TESTING INSIGHTDECK APPROACH")
    print("="*70)
    
    try:
        from langgraph_agent import run_langgraph_analysis
        
        # Sample transcript
        sample_transcript = """
        Team Lead: We've been struggling with our current project management setup.
        The tools we use don't really integrate well with each other.
        
        Interviewer: Can you tell me more about the specific pain points?
        
        Team Lead: Sure. The biggest issue is context switching. We use Jira for 
        tickets, Slack for communication, Confluence for docs, and Zoom for meetings.
        Nothing talks to each other, so we're constantly copying information around.
        It takes probably 30% of my day just keeping things in sync.
        
        Interviewer: How does this affect your team?
        
        Team Lead: It's frustrating for everyone. Junior team members especially get 
        lost because information is scattered. And when someone's on vacation, nobody 
        can find anything. We need something more integrated.
        """
        
        result = run_langgraph_analysis(
            transcript=sample_transcript,
            research_question="user experience with project management tools",
            target_demographic="remote team leaders"
        )
        
        return result
    except Exception as e:
        print(f"❌ InsightDeck test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_results(cerebras_result, insightdeck_result):
    """Compare the results from both approaches"""
    print("\n" + "="*70)
    print("📊 COMPARISON RESULTS")
    print("="*70)
    
    print("\n### Cerebras Approach:")
    print("-" * 70)
    if cerebras_result:
        print(f"Interviews: {len(cerebras_result.get('all_interviews', []))}")
        print(f"Synthesis length: {len(cerebras_result.get('synthesis', ''))} chars")
        print(f"\nFirst 300 chars of synthesis:")
        print(cerebras_result.get('synthesis', '')[:300] + "...")
    else:
        print("❌ No results available")
    
    print("\n### InsightDeck Approach:")
    print("-" * 70)
    if insightdeck_result:
        print(f"Interviews: {len(insightdeck_result.get('all_interviews', []))}")
        print(f"Themes: {len(insightdeck_result.get('key_themes', []))}")
        print(f"Synthesis length: {len(insightdeck_result.get('synthesis', ''))} chars")
        print(f"Processing time: {insightdeck_result.get('processing_time', 0):.1f}s")
        print(f"\nFirst 300 chars of synthesis:")
        print(insightdeck_result.get('synthesis', '')[:300] + "...")
    else:
        print("❌ No results available")
    
    print("\n" + "="*70)
    print("🎯 KEY DIFFERENCES")
    print("="*70)
    print("""
    Cerebras:
    - Synthetic personas (10 interviews)
    - Pure text-based research
    - Ultra-fast inference
    - Good for ideation
    
    InsightDeck:
    - Real transcript analysis
    - Combines real + synthetic data
    - Deeper reasoning with Claude
    - Production-ready for UX research
    """)

if __name__ == "__main__":
    print("\n🔬 CEREBRAS vs INSIGHTDECK COMPARISON TEST")
    print("This will run both approaches and compare results")
    print()
    
    # Note: This might take 3-5 minutes total
    print("⏱️  Note: This may take 3-5 minutes to complete both tests")
    print()
    
    # Test both approaches
    cerebras_result = test_cerebras()
    insightdeck_result = test_insightdeck()
    
    # Compare results
    compare_results(cerebras_result, insightdeck_result)
    
    print("\n✅ Comparison complete!")
