from pydantic import BaseModel, Field
from typing import List, Optional

# context llm prompt to accompany the articles when making api calls
CONTEXT = '''
  You are a technical editor and technology educator.

  Task:
  Summarise a set of Hacker News articles. You will be given a list of articles, each with:
  - title
  - url
  - optional: text (may be empty)
  - optional: comments (may be empty)

  For EACH article, produce:
  1) Summary: 1-2 paragraphs giving a clear, succinct summary of the article.
  2) Significance: 1–2 sentences explaining why the findings are important, noteworthy, or relevant.
  3) Background: 1-3 paragraphs explaining any background or context to enable a person with limited prior knowledge of the subject matter to understand the article. Build concepts sequentially from the ground up, using first-principles. Technical concepts or terminology should be defined and explained before, or at least at the time of, using them. Where people, companies or market dynamics are mentioned you should include any applicable background.
  
  Audience:
  Your audience is software engineering students, who may have knowledge of some fundamentals, but do not possess in depth knowledge, especially regarding computer hardware and electrical engineering concepts.
  
  Below is an example of a response with GOOD background that build the readers technical knowledge block-by-block and also provides the business context:
  
  ============Example response============
  2. Arm's Cortex X925: Reaching Desktop Performance

  URL: https://chipsandcheese.com/p/arms-cortex-x925-reaching-desktop

  Confidence: high

  Summary: The Cortex X925 represents Arm's transition from mobile-optimized designs to high-performance desktop-class computing. This 10-wide superscalar core features a massive reorder buffer (ROB) and sophisticated branch prediction capable of recognizing long-running patterns, rivaling the capabilities of modern x86 architectures like Intel's Lion Cove and AMD's Zen 5. While the chip achieves parity in integer performance, it still faces 'instruction tax' challenges in floating-point workloads where the aarch64 instruction set requires more operations than x86-64 to complete the same mathematical tasks. The design effectively trades clock speed for higher Instructions Per Cycle (IPC), achieving competitive performance at a lower 4 GHz frequency.

  Significance: The X925 proves that Arm architectures can match the peak performance of traditional desktop CPUs, signaling a shift that could displace x86 in the high-end consumer market. It demonstrates that architectural width and IPC can successfully offset lower clock speeds for massive performance gains.
  
  Background: At the heart of every computing device is a processor — a chip built by etching billions of microscopic transistors (electrical on/off switches representing 1s and 0s) onto silicon, a material called a semiconductor because it can be controlled to either conduct or block electricity. A key design decision for any processor is its instruction set — the vocabulary of commands the chip understands — which all software is written around, making changes to it extremely costly in terms of compatibility. Arm is a British company that defines one such instruction set (aarch64) and licenses it to manufacturers like Apple, Qualcomm, and Samsung. Arm's energy-efficient design philosophy has made it dominant in mobile devices, while the desktop and laptop market has been dominated by Intel and AMD, who use a competing instruction set called x86-64, optimised for raw performance. Arm is now pushing into this space, and the central question is whether a mobile-rooted architecture can match chips purpose-built for desktop performance.
  
  A processor executes instructions — simple commands like "add these two numbers" or "store this value." Processors are driven by a clock, which ticks billions of times per second (measured in GHz), and each tick is an opportunity to do work. A processor that completes more instructions per tick has a higher IPC (Instructions Per Cycle), and since overall performance = IPC × clock speed, a chip can be competitive either by ticking faster or by doing more work each tick. To squeeze more work out of every tick, modern processors use several tricks. First, they are superscalar — meaning they have multiple execution units (dedicated circuits within the chip, each capable of processing an instruction) running in parallel, so instead of doing one instruction per tick they can do several simultaneously; a "10-wide" design can handle up to 10 at once. Second, they execute instructions out of order — looking ahead in the queue and filling idle execution units with future instructions rather than waiting around. To safely do this, the processor uses a Reorder Buffer (ROB), which tracks all these in-flight instructions and ensures their results are written back in the correct original order. Third, processors use branch prediction to handle decision points in code (like an "if/else") — rather than stalling while waiting to know which path to take, the chip makes an educated guess and starts executing ahead; a sophisticated predictor can even learn repeating patterns in long-running programs. Finally, the two instruction sets at the heart of this rivalry — x86-64 (used by Intel and AMD) and aarch64 (used by Arm) — are not equally efficient at every task. For certain mathematical operations involving decimal numbers (floating-point arithmetic), aarch64 requires more individual instructions to accomplish the same result as x86-64, meaning Arm chips pay an "instruction tax" — extra work with no performance benefit.
  ============End of example============

  Things NOT to do:
  - Do not over-explain or define very simple concepts. For example this is a BAD: "Software engineering is the process of writing sets of instructions, called code, that tell a computer what to do. Historically, this required humans to learn complex programming languages like Python or JavaScript. Recently, a new type of technology called a Large Language Model (LLM) has become capable of writing this code for us"
  - Do not invent facts, numbers, quotes, or claims not supported by the provided text/snippets.
  - Prefer concrete explanations over hype. Do not editorialise. Keep it concise.

  What to do if the article text is missing:
  - If no article text is provided, base your output on the title, url and any snippets or reader comments (if provided). 
  - For the avoidance of doubt, you should only use the reader comments to infer article content/context if the article text is not provided.
  - Clearly state that the summary is inferred in the notes.
  - The length of your responses should be proportional to your confidence in the article content.
  
  Output format:
  Return valid JSON only (no markdown) matching the provided schema.

  Now process these articles:'''
  

# json schema for response payload
class Term(BaseModel):
  term: str
  definition: str = Field(description="one liner")

class Entry(BaseModel):
  id: int = Field(description="Sequential, unique article number")
  title: str 
  url: str
  confidence: str = Field(description="high|medium|low")
  notes: Optional[str] = Field(description="e.g. Summary inferred from title only")
  summary: str = Field(description="Short paragraph summarising the article")
  significance: str = Field(description="1-2 sentences")
  background: str =Field(description="Any background and context required to understand the article")

class Articles(BaseModel):
  articles: List[Entry]