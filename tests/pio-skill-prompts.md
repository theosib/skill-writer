# Starter Prompts for PIO Skill Creation

Use these in a fresh Claude Code session with skill-writer installed.

## Prompt 1: Kick off with skill-writer

```
/skill-writer "Expert PIO programming skill for RP2040/RP2350 — writing PIO assembly, DMA integration, advanced techniques like instruction injection"
```

## Prompt 2: Answer the interview questions

When skill-writer asks its Phase 1 questions, provide these answers (adapt as needed):

```
1. WHAT: Makes Claude an expert at writing PIO assembly programs for the RP2040/RP2350, including state machine configuration, DMA setup, and advanced techniques like runtime instruction injection.

2. TRIGGERS: When working on RP2040/RP2350 projects involving PIO, when writing .pio files, when configuring DMA for PIO transfers, when asked about state machine programming, when debugging PIO timing issues.

3. INPUTS: Description of the I/O protocol or peripheral to implement. Optionally: timing requirements, pin assignments, clock divider constraints, number of state machines available.

4. OUTPUT: Complete PIO programs (.pio format) with matching C SDK setup code, DMA configuration when appropriate, and comments explaining timing and pin behavior. Should include the pio_add_program / sm_config boilerplate.

5. CONSTRAINTS:
   - Must be accurate to RP2040 hardware: 32 instructions max per PIO program, 4 state machines per PIO block, side-set bits steal from delay bits
   - Must handle DMA correctly: DMA has no infinite transfer count — address the two main solutions (ping-pong buffers with chained channels, or timer-triggered re-arm)
   - Should know RP2040 vs RP2350 PIO differences (RP2350 has more instructions, different pin mapping)
   - Must understand PIO clock divider math (system clock / desired frequency)

6. CROSS-MODEL: Claude Code primarily, but the domain knowledge should be written so it could work on other models too. Don't assume the model knows PIO internals — state facts explicitly.
```

## Prompt 3: Request deep research before writing

```
Before writing the skill, do deep research first. This is a specialized hardware domain and the skill needs to encode expert-level knowledge. Use subagents to search in parallel:

RESEARCH TRACK 1 — Core PIO patterns:
- Search GitHub for popular RP2040 PIO examples (pico-examples repo, community projects)
- Catalog common patterns: UART, SPI, I2C, WS2812B, VGA, audio PWM, logic analyzer
- For each pattern, note: instruction count, clock divider, autopush/autopull settings, pin mapping

RESEARCH TRACK 2 — DMA integration:
- How to set up DMA channels for PIO TX/RX FIFOs
- The infinite transfer count problem and solutions (ping-pong/chained channels, timer re-arm, ring buffer with wrap)
- DMA pacing with PIO DREQ signals
- Double-buffering patterns

RESEARCH TRACK 3 — Advanced techniques:
- CPU injecting instructions into PIO at runtime (sm_exec)
- One PIO block injecting instructions into another
- Using the instruction memory as a lookup table
- Dynamic pin remapping tricks
- Using IRQ flags for synchronization between state machines
- Self-modifying PIO programs (MOV EXEC)

RESEARCH TRACK 4 — Pitfalls and debugging:
- Common timing mistakes (forgetting side-set steals delay bits)
- FIFO stall behaviors
- Clock divider precision limits
- Debugging with logic analyzers
- The 32-instruction limit and workarounds (multiple state machines cooperating)

RESEARCH TRACK 5 — RP2350 differences:
- Extended instruction set
- Additional PIO blocks
- Pin mapping changes
- Backward compatibility considerations

Save all research findings to files before proceeding to write the skill:
- research/pio-patterns.md
- research/dma-integration.md
- research/advanced-tricks.md
- research/pitfalls.md
- research/rp2350-differences.md
```

## Prompt 4: Provide your own examples

```
Here are some advanced PIO techniques I've used or collected. Incorporate these into the skill's knowledge:

[paste your examples of instruction injection, PIO-to-PIO injection, etc.]
```

## Prompt 5: Write the skill with progressive disclosure

```
Now write the skill. Structure it as:
- SKILL.md (≤300 lines): Core rules, instruction set reference, process steps
- references/pio-patterns.md: Common protocol implementations with annotated examples
- references/dma-guide.md: DMA setup patterns and the infinite-count solutions
- references/advanced-techniques.md: Instruction injection, synchronization, creative uses
- references/pitfalls.md: Common mistakes with explanations

The SKILL.md should be compact enough to fit in context alongside a real project, but the references should be thorough. A developer should be able to write any common PIO program from the skill alone, and handle unusual cases by loading the reference files.
```

## Prompt 6: Validate with a concrete test

```
Test the skill: pretend you've never seen it before. Using only the SKILL.md content, write a PIO program that implements a WS2812B LED strip driver with DMA for continuous updates from a frame buffer. Include the complete .pio file and C setup code.

Then check: Is the timing correct for WS2812B (800kHz, specific T0H/T1H/T0L/T1L)? Is the DMA configured correctly? Does it handle the infinite-transfer problem?
```
