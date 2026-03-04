from pydantic import BaseModel, Field
from typing import List, Optional

# context llm prompt to accompany the articles when making api calls
CONTEXT = '''
  You are a technical editor and technology educator.

  Task:
  Summarise a set of Hacker News articles. You will be given a list of articles, each with:
  - title
  - url
  - optional: extracted_text (may be empty)

  For EACH article, produce:
  1) Summary: 1-2 paragraphs giving a clear, succinct summary of the article.
  2) Significance: 1–2 sentences explaining why the findings are important, noteworthy, or relevant.
  3) Background: 1-3 paragraphs explaining any background or context to enable a person without prior knowledge of the subject matter to understand the article. Build concepts sequentially from the ground up, using first-principles. Technical concepts or terminology should be defined and explained before, or at least at the time of, using them. Where companies or market dynamics are mentioned you should include any applicable background. Don't assume the reader knows the company or market.
  
  Below is an example of a response with a GOOD background that builds the readers technical knowledge step-by-step and also provides the business context:
  
  ============Example responses============
  2. Arm's Cortex X925: Reaching Desktop Performance

  URL: https://chipsandcheese.com/p/arms-cortex-x925-reaching-desktop

  Confidence: high

  Summary: The Cortex X925 represents Arm's transition from mobile-optimized designs to high-performance desktop-class computing. This 10-wide superscalar core features a massive reorder buffer (ROB) and sophisticated branch prediction capable of recognizing long-running patterns, rivaling the capabilities of modern x86 architectures like Intel's Lion Cove and AMD's Zen 5. While the chip achieves parity in integer performance, it still faces 'instruction tax' challenges in floating-point workloads where the aarch64 instruction set requires more operations than x86-64 to complete the same mathematical tasks. The design effectively trades clock speed for higher Instructions Per Cycle (IPC), achieving competitive performance at a lower 4 GHz frequency.

  Significance: The X925 proves that Arm architectures can match the peak performance of traditional desktop CPUs, signaling a shift that could displace x86 in the high-end consumer market. It demonstrates that architectural width and IPC can successfully offset lower clock speeds for massive performance gains.
  
  Background: At the heart of every computing device is a processor — a chip built by etching billions of microscopic switches called transistors onto a sliver of silicon. Each transistor can be switched on or off electrically, representing a 1 or a 0, and by combining billions of them together a processor can perform complex calculations at enormous speed. The material that makes this possible — silicon — is called a semiconductor because it can be controlled to either conduct or block electricity, giving engineers precise control over those billions of switches. Designing these processors is an enormously complex undertaking, and one of the key decisions is choosing an instruction set — the vocabulary of commands the chip will understand. Different companies can design chips around the same instruction set, which matters because all software is written to speak a particular instruction set's language; changing it would break compatibility with existing programs.
  
  Arm is a British company that defines one such instruction set (called aarch64) and licenses it to other companies — like Apple, Qualcomm, and Samsung — who then design and manufacture their own chips built around that shared vocabulary. This model has made Arm dominant in mobile devices like phones and tablets, where their instruction set's energy-efficient design philosophy is ideal for battery-powered hardware. The desktop and laptop market, however, has historically been dominated by Intel and AMD, two American companies whose chips use a competing instruction set called x86-64, purpose-built for raw performance over efficiency. Arm is now pushing into that high-performance desktop space, and the question is whether a design rooted in mobile efficiency can genuinely match chips that have been optimised for decades for desktop performance.
  
  To understand how that comparison is actually measured, it helps to know how processor performance works. A processor executes instructions — simple commands like "add these two numbers" or "store this value." Processors are driven by a clock, which ticks billions of times per second (measured in GHz), and each tick is an opportunity to do work. A processor that completes more instructions per tick has a higher IPC (Instructions Per Cycle), and since overall performance = IPC × clock speed, a chip can be competitive either by ticking faster or by doing more work each tick. To squeeze more work out of every tick, modern processors use several tricks. First, they are superscalar — meaning they have multiple execution units (dedicated circuits within the chip, each capable of processing an instruction) running in parallel, so instead of doing one instruction per tick they can do several simultaneously; a "10-wide" design can handle up to 10 at once. Second, they execute instructions out of order — looking ahead in the queue and filling idle execution units with future instructions rather than waiting around. To safely do this, the processor uses a Reorder Buffer (ROB), which tracks all these in-flight instructions and ensures their results are written back in the correct original order, like a waiter who prepares multiple dishes simultaneously but always serves them in the order they were requested. Third, processors use branch prediction to handle decision points in code (like an "if/else") — rather than stalling while waiting to know which path to take, the chip makes an educated guess and starts executing ahead, like a navigator on a road trip who begins preparing for the most likely upcoming turn before being told which way to go; a sophisticated predictor can even learn repeating patterns in long-running programs. Finally, the two instruction sets at the heart of this rivalry — x86-64 (used by Intel and AMD) and aarch64 (used by Arm) — are not equally efficient at every task. For certain mathematical operations involving decimal numbers (floating-point arithmetic), aarch64 requires more individual instructions to accomplish the same result as x86-64, meaning Arm chips pay an "instruction tax" — extra work with no performance benefit.
  
  
  2. Intel's make-or-break 18A process node debuts for data center with 288-core Xeon

  URL: https://www.tomshardware.com/pc-components/cpus/intels-make-or-break-18a-process-node-debuts-for-data-center-with-288-core-xeon-6-cpu-multi-chip-monster-sports-12-channels-of-ddr5-8000-foveros-direct-3d-packaging-tech

  Confidence: high

  Summary: Intel has unveiled its 'Clearwater Forest' Xeon 6+ processors, the first data center CPUs manufactured using the company's critical 18A (1.8nm-class) fabrication process. This massive processor features up to 288 energy-efficient 'Darkmont' cores spread across 12 compute chiplets. The architecture uses Intel's Foveros Direct 3D packaging to stack these compute tiles vertically on top of active base tiles, while lateral connections are managed by EMIB bridges. Designed for high-density environments like telecom and cloud providers, the chip includes over 1GB of last-level cache to reduce data bottlenecks and supports 12 channels of DDR5-8000 memory. The Darkmont cores themselves have been upgraded with broader instruction pipelines and deeper 'out-of-order' engines to improve how many tasks they can handle simultaneously.

  Significance: This is the first major product on Intel's 18A node, a 'make-or-break' technology generation intended to restore Intel's leadership in semiconductor manufacturing against TSMC. The use of 288 cores and advanced 3D stacking demonstrates Intel's ability to create high-density, modular chips for the growing demands of cloud and edge AI infrastructure.
  
  Background: Every processor is built by etching billions of microscopic switches called transistors onto a sliver of silicon — a material called a semiconductor because it can be controlled to either conduct or block electricity. Each transistor switches on or off electrically, representing a 1 or a 0, and by combining billions of them a processor performs complex calculations at speed. The generation of manufacturing technology used to etch these transistors is called a process node — when Intel says "18A" or "1.8nm," they are describing how small and densely packed those transistors are. Smaller transistors mean more can fit in the same space, making chips either more powerful or more energy efficient. Two companies dominate the business of actually manufacturing these chips at scale: Intel, an American company that both designs and manufactures its own processors, and TSMC (Taiwan Semiconductor Manufacturing Company), a Taiwanese company that manufactures chips on behalf of other companies including Apple, Nvidia, and AMD. Through the late 2010s, Intel fell behind TSMC in manufacturing capability — rival chips were being built on more advanced nodes, with smaller, denser transistors. Intel's 18A node is its attempt to close that gap and reclaim parity with TSMC's most advanced manufacturing processes.
  
  As chips grow more complex, manufacturing them as a single large piece of silicon becomes impractical — a single microscopic defect ruins the entire chip, and larger chips mean more defects and lower yields. The solution is chiplets: instead of one large chip, engineers design several smaller ones and connect them together in a single package. Intel uses two technologies to do this. EMIB (Embedded Multi-die Interconnect Bridge) connects chiplets that sit side-by-side horizontally, acting as a high-speed bridge buried within the base of the package. Foveros handles the vertical dimension — it is a 3D stacking technology that allows chiplets to be placed directly on top of one another, with data travelling up and down between layers. Together, EMIB manages lateral connections and Foveros manages vertical ones, allowing Intel to assemble a large, complex processor from smaller, more manufacturable pieces.
  
  Inside the processor, performance depends not just on the number of cores but on how efficiently data is fed to them. Each core executes instructions — simple commands like "add these two numbers" — and modern cores use wider instruction pipelines (the ability to process more instructions simultaneously) and deeper out-of-order execution (looking ahead in the instruction queue to keep execution units busy rather than waiting) to maximise throughput. But cores can only work as fast as data arrives, so processors use cache — a small, fast pool of memory built directly onto the chip — to store frequently needed data close to the cores, avoiding the much slower round-trip to main system RAM. Cache exists at multiple levels: small caches local to each individual core for speed, and a larger shared last-level cache accessible to all cores. With 288 cores operating simultaneously, Intel includes over 1GB of shared last-level cache to prevent cores sitting idle waiting for data. Data that isn't in cache must travel from main RAM into the processor through memory channels — parallel pathways that move data simultaneously; 12 channels means 12 streams of data flowing in at once. DDR5-8000 refers to the type and speed of RAM being used — DDR5 is the latest generation of memory standard, and 8000 refers to its data transfer rate (8000 megatransfers per second), roughly double the speed of previous generation memory.
  
  ============End of examples============



  Rules:
  - Use only the information provided in the input. If the article content is missing, base your output on the title + any snippets, and clearly state that the summary is inferred.
  - Do not invent facts, numbers, quotes, or claims not supported by the provided text/snippets.
  - Prefer concrete explanations over hype. Keep it concise.

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