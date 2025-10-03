# 🧪 Cerebras User Research Automation - Test Branch

This directory contains the **original Cerebras approach** for comparison with our enhanced InsightDeck Agent implementation.

## 📋 What's Here

This is a direct implementation of the Cerebras cookbook example from:
https://inference-docs.cerebras.ai/cookbook/agents/automate-user-research

## 🔄 Key Differences: Cerebras vs InsightDeck

| Feature | Cerebras Original | InsightDeck Enhanced |
|---------|------------------|---------------------|
| **Input** | Text prompts only | Real audio files + transcription |
| **LLM** | Cerebras Llama 3.3 70B | Anthropic Claude 3.5 Sonnet |
| **Speed** | Ultra-fast (Cerebras hardware) | Slower but deeper reasoning |
| **Interviews** | 10 synthetic personas | 5 personas + real transcript analysis |
| **Audio Support** | ❌ None | ✅ Whisper + ElevenLabs diarization |
| **Use Case** | Synthetic research | Real user research automation |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From the cerebras_example directory
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit your `.env` file (in project root):

```bash
# For original Cerebras approach (fastest)
CEREBRAS_API_KEY=your_cerebras_key_here

# OR fallback to OpenAI
OPENAI_API_KEY=your_openai_key_here

# OR fallback to Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
```

**Get Cerebras API Key:**
- Sign up at: https://cloud.cerebras.ai/
- Free tier available for testing
- Llama 3.3 70B is incredibly fast on their hardware

### 3. Run the Example

```bash
python automate_user_research.py
```

## 📊 What It Does

1. **Configuration Node** - Generates interview questions
2. **Persona Generator** - Creates 10 diverse user personas
3. **Interview Agent** - Conducts synthetic interviews
4. **Synthesis Agent** - Analyzes patterns and generates insights

### Sample Output

```
🔧 Configuring research: developer experience with AI coding assistants
📊 Planning 10 interviews with 5 questions each
✅ Generated 5 questions

👥 Creating 10 personas...
Persona 1: Alex Chen (28, Software Engineer)
Persona 2: Maria Rodriguez (35, Senior Developer)
...

💬 Interview 1/10 - Alex Chen
Q1: How has AI changed your daily coding workflow?
A: It's been transformative but also requires careful oversight...

🧠 Analyzing all interviews...
🎯 COMPREHENSIVE RESEARCH INSIGHTS
```

## 🎯 Testing Strategy

### Compare Approaches:

1. **Run Cerebras version** (this directory):
   ```bash
   python automate_user_research.py
   ```
   - Note: Speed, number of personas, insight depth

2. **Run InsightDeck version** (parent directory):
   ```bash
   cd ..
   python langgraph_agent.py
   ```
   - Note: Integration with real transcripts, agent specialization

3. **Compare Results:**
   - Cerebras: Fast, synthetic, good for ideation
   - InsightDeck: Slower, real data, better for actual research

## 💡 Insights from Testing

### Cerebras Strengths:
- ⚡ **Speed** - Incredibly fast inference
- 🎭 **Synthetic Personas** - Great for quick exploration
- 💰 **Cost** - Very affordable per token
- 🔄 **Iteration** - Rapid prototyping

### Cerebras Limitations:
- ❌ No real audio/transcript processing
- ❌ Focused on synthetic interviews only
- ❌ Less depth in analysis (optimized for speed)
- ❌ Requires separate audio transcription step

### InsightDeck Advantages:
- ✅ End-to-end (audio → insights → presentation)
- ✅ Real user data, not synthetic
- ✅ Speaker diarization built-in
- ✅ Deeper analysis with Claude
- ✅ Web interface for non-technical users

## 🔧 Customization

Edit these constants in `automate_user_research.py`:

```python
DEFAULT_NUM_INTERVIEWS = 10  # Number of personas to create
DEFAULT_NUM_QUESTIONS = 5    # Questions per interview
```

Smaller numbers = faster testing:
```python
DEFAULT_NUM_INTERVIEWS = 3   # Quick test
DEFAULT_NUM_QUESTIONS = 3    # Quick test
```

## 📚 Learning Points

### What We Adopted:
1. **LangGraph state machine** - Clean orchestration
2. **Specialized nodes** - Single responsibility principle
3. **Persona generation** - Synthetic user creation
4. **Conditional routing** - Smart workflow decisions

### What We Enhanced:
1. **Real audio integration** - Whisper + ElevenLabs
2. **Claude reasoning** - Better for UX research
3. **Quality validation** - Accuracy checking
4. **Web interface** - Accessibility for researchers
5. **Presentation generation** - Complete workflow

## 🔄 Switch Back to Main Branch

When done testing:

```bash
# Go back to main branch
cd ..
git checkout master

# Or stay on test branch
git checkout cerebras-test
```

## 📝 Notes

- This is a **faithful recreation** of the Cerebras approach
- Uses same LangGraph patterns and state management
- Falls back to OpenAI/Anthropic if Cerebras not available
- Pure synthetic interviews - no real data processing
- Great for understanding the original architecture

## 🎯 Recommendation

**Use Cerebras approach for:**
- Quick ideation and exploration
- Synthetic user research
- Rapid prototyping
- High-volume low-depth analysis

**Use InsightDeck for:**
- Real user interviews
- Audio/video transcription
- Professional presentations
- Comprehensive UX research
- Stakeholder deliverables

---

**Both approaches have value!** This comparison helps demonstrate your understanding of the space and thoughtful integration choices.
