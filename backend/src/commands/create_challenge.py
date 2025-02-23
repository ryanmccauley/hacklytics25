from mediator import MediatorDTO, mediator
from models.enums import ChallengeCategory, ChallengeDifficulty
from models.entities import Challenge, ChallengeFile
from database.mongo import engine
from typing import Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field
from settings import global_settings
from odmantic import ObjectId
from langchain_core.prompts import PromptTemplate

class CreateChallengeCommand(MediatorDTO):
  category: ChallengeCategory
  difficulty: ChallengeDifficulty
  additional_prompt: Optional[str] = None

class CreateChallengeResponse(MediatorDTO):
  challenge_id: ObjectId

class ChallengeOuptut(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  title: str
  setup_instructions: str = Field(description="List of instructions for the user to setup the challenge on their environment. This will be stored in an README.md file")
  description: str = Field(description="A short one to two sentence description of the challenge")
  flag_solution: str = Field(description="The solution to the challenge")
  files: list[ChallengeFile]


@mediator.register_handler(CreateChallengeCommand)
async def create_challenge(command: CreateChallengeCommand) -> CreateChallengeResponse:
  outline = await create_challenge_outline(command)
  output = await create_challenge_output(outline)

  challenge = Challenge(
    id=ObjectId(),
    category=command.category,
    difficulty=command.difficulty,
    title=output.title,
    setup_instructions=output.setup_instructions,
    description=output.description,
    flag_solution=output.flag_solution,
    files=output.files
  )

  await engine.save(challenge)

  return CreateChallengeResponse(challenge_id=challenge.id)

async def create_challenge_outline(command: CreateChallengeCommand) -> str:
  """
  Create a challenge outline for a given challenge category and difficulty.

  Args:
    command: CreateChallengeCommand

  Returns:
    str
  """

  model = ChatOpenAI(model="o3-mini-2025-01-31", api_key=global_settings.OPENAI_API_KEY, max_completion_tokens=4096)
  prompt = PromptTemplate.from_template("""
    You are an Instant CTF Agent Generator responsible for creating a custom outline for a CTF challenge. Your output is a structured outline that will later be used to generate the final output files (challenge instructions and setup instructions). This outline must clearly determine:
1. What kind of challenge within the given category should be developed.
2. What code components and technical steps are needed to implement this challenge.

User Request Details:
- Category: {category}
    *Example values: "Web Exploitation", "Reverse Engineering", "SQL Injection"*
- Difficulty: {difficulty}
    *Example values: "Easy", "Medium", "Hard", "Impossible"*
- Additional Information (Optional): {additional_prompt}
    *This field may contain extra guidelines or specific elements to incorporate.*

Instructions:
1. **Outline Creation:**  
   Based on the provided `[challenge_category]`, `[difficulty_level]`, and optional `[additional_info]`, generate a comprehensive outline that includes:
   - A clear description of the specific type of challenge to be developed. Explain why this challenge fits the selected category and difficulty.
   - A detailed list or explanation of the code components, scripts, frameworks, and configurations needed to build the challenge.
   
2. **Jurassic World Theme:**  
   Infuse the outline with language and design cues inspired by Jurassic World. Your challenge description and technical implementation should evoke prehistoric landscapes, dinosaur motifs, and adventurous exploration—imagine challenges set within a digital dinosaur park where every vulnerability is another wild creature to outsmart.

3. **Preparation for Output Files:**  
   Remember that the outline you generate will be used to create:
   - **Challenge Instructions:** A detailed description of the challenge that guides the user.
   - **Setup Instructions:** Clear, step-by-step instructions on how to deploy and interact with the challenge.
   Your outline must be actionable, logically organized, and serve as a robust blueprint for both.

4. **Clarity and Detail:**  
   Structure your outline using headers and bullet points as needed. Clearly separate the challenge description from the technical/code requirements. Provide as much detail as possible to ensure the next generation step has all the information required to build and verify the challenge.

----------------------------------------
Example Structure:
----------------------------------------
Title: Jurassic CTF Challenge Outline

I. Challenge Description
   - Detailed explanation of the challenge type, how it fits within `[challenge_category]`, and why it is appropriate for a `[difficulty_level]` challenge.
   - Integration of any extra details from `[additional_info]`.
   - Immersive, thematic language that evokes a Jurassic World setting. For example: “Imagine a digital landscape where every click takes you deeper into a forgotten park filled with ancient secrets and lurking dangers…”
   
II. Technical Implementation
   - A thorough list of code components, libraries, frameworks, scripts, and configurations required.
   - An explanation of how these technical elements combine to deliver the challenge. Include any specific instructions that might help with debugging or iterative testing.
   
III. Additional Considerations
   - Any extra guidelines or creative directions based on `[additional_info]`.
   - Suggestions for potential pitfalls or hints for users that align with the Jurassic theme.

----------------------------------------
Detailed Examples:
----------------------------------------

**A. Web Exploitation Examples (PicoCTF–style):**

1. *Easy – “Jurassic Safari’s Secret”*  
   - **Challenge Description:**  
     In this introductory challenge, users encounter a seemingly simple dinosaur-themed webpage. The page contains hidden HTML comments and a poorly secured source code. The challenge is to inspect the webpage’s source code to find a hidden string resembling a flag.  
   - **What the User Must Do:**  
     The user is expected to open the browser’s developer tools, inspect the page’s HTML, and discover a commented section with a flag (e.g., `FLAG...`). Detailed hints may point to checking the `<head>` or `<footer>` for any “secret” code.  
   - **Technical Implementation:**  
     The outline should include instructions for creating a static webpage with embedded comments, ensuring the flag is visible only in the source code, and integrating a Jurassic background image and dinosaur icons.

2. *Medium – “Raptor’s Roost Vulnerability”*  
   - **Challenge Description:**  
     This challenge raises the stakes by presenting a web application that is vulnerable to reflected Cross-Site Scripting (XSS). The page, styled as a raptor observation log, accepts user input and echoes it back unsanitized.  
   - **What the User Must Do:**  
     The user must discover the vulnerability by inputting malicious scripts into a search field, triggering the execution of JavaScript that reveals a hidden flag. They are expected to use browser developer tools and a basic understanding of XSS to craft a payload that exposes the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should detail the setup of a simple web server (using Flask or Node.js) with an input field, deliberately omitting sanitization. It should also specify how to integrate Jurassic-themed elements such as fossilized logs and raptor silhouettes.

3. *Hard – “Dilophosaurus Denial”*  
   - **Challenge Description:**  
     In this challenge, users face a more complex web application where a combination of URL manipulation and hidden parameters lead to a sensitive endpoint. The site, designed as a digital replica of a dinosaur research facility, hides its flag behind a misconfigured access control.  
   - **What the User Must Do:**  
     The challenge requires the user to manipulate URL parameters, analyze network traffic using tools like Burp Suite, and piece together clues from server responses. The flag may be split across multiple responses (e.g., `FLAG...` in one response and `phosaurus` in another), requiring the user to combine these pieces correctly.  
   - **Technical Implementation:**  
     Outline the code components for the vulnerable endpoint, including instructions for setting up routing and session handling. Detail how the misconfiguration (such as improper validation of session tokens) is embedded intentionally and provide guidelines for integrating detailed Jurassic UI elements like lab environments and digital fossils.

4. *Impossible – “Tyrannosaurus Terminal Takeover”*  
   - **Challenge Description:**  
     The ultimate web exploitation challenge involves a multi-layered vulnerability chain. In this scenario, the user navigates a complex dinosaur park management system that is protected by advanced security measures. The challenge combines SQL injection, file inclusion, and cross-site scripting, all hidden within a futuristic Jurassic World interface.  
   - **What the User Must Do:**  
     The user must identify the chain of vulnerabilities, starting with an obfuscated parameter that leads to a SQL injection, then leverage the data retrieved to execute a file inclusion attack that eventually reveals a heavily encoded flag. This flag might be spread across multiple modules and require decoding.  
   - **Technical Implementation:**  
     The outline should specify a modular code structure where each vulnerability is isolated but interconnected. Include detailed instructions on how to simulate secure coding practices with intentional flaws and how to design a rich, cinematic Jurassic interface that includes elements like interactive maps of a dinosaur park and advanced error logging.

**B. Reverse Engineering Examples:**

1. *Easy – “Dino Egg Decoder”*  
   - **Challenge Description:**  
     This challenge features a small binary (or obfuscated script) that, when executed, prints a scrambled message. Set in a Jurassic laboratory, the task is to decode a reversed string to reveal the flag.  
   - **What the User Must Do:**  
     The user should use tools such as the `strings` command or a simple disassembler to extract the hidden flag (e.g., `FLAG...`) from the binary’s output.  
   - **Technical Implementation:**  
     The outline should include instructions to compile a simple C program or package a Python script that intentionally reverses a known string. Ensure the code includes dinosaur-themed comments and imagery in its output.

2. *Medium – “Triceratops Lock”*  
   - **Challenge Description:**  
     Here, a binary mimics a digital lock system for a dinosaur enclosure. The program checks for a specific input password using a hard-coded algorithm.  
   - **What the User Must Do:**  
     The user must analyze the binary with tools like Ghidra or IDA Pro to understand the password-checking algorithm. Once they deduce the logic, they must determine the correct password (e.g., `FLAG...`) to unlock the “dino gate.”  
   - **Technical Implementation:**  
     Outline the process for creating a binary that uses a simple, custom algorithm for password verification. Include comments in the code referencing dinosaur traits (e.g., “as sturdy as a triceratops”) and instructions for debugging.

3. *Hard – “Velociraptor Vault”*  
   - **Challenge Description:**  
     This challenge presents a heavily obfuscated binary designed to simulate a secure vault inside a velociraptor habitat. The binary employs anti-debugging techniques and encrypted routines.  
   - **What the User Must Do:**  
     The user must perform both static and dynamic analysis to bypass anti-debugging measures, decrypt critical routines, and ultimately extract the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     Provide a detailed list of technical steps including the use of debuggers, runtime analysis, and deobfuscation techniques. The outline should mention the integration of Jurassic elements by including dinosaur roar sound effects or graphics in the UI when certain conditions are met.

4. *Impossible – “Mosasaurus Matrix”*  
   - **Challenge Description:**  
     The most challenging reverse engineering task, this binary is deliberately engineered to be nearly impenetrable. Featuring virtualization or heavy obfuscation techniques, it simulates the complexity of a Mesolithic predator’s behavior.  
   - **What the User Must Do:**  
     The user must combine advanced disassembly, dynamic analysis, and creative problem-solving to understand a layered virtual machine or obfuscated control flow, and then reconstruct the logic to extract the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should detail an advanced build process that employs multiple layers of obfuscation, anti-tampering checks, and custom encryption routines. Emphasize the need for an in-depth guide on debugging and overcoming virtualized code, with the interface featuring high-detail Jurassic-themed graphics and animations.

**C. SQL Injection Examples:**

1. *Easy – “Jurassic Login”*  
   - **Challenge Description:**  
     In this basic challenge, users encounter a login page for a dinosaur park management system. The login form is vulnerable to a simple SQL injection where a classic payload (e.g., `1' OR '1'='1`) bypasses authentication.  
   - **What the User Must Do:**  
     The user must identify the injection point, craft the correct payload, and log in to reveal a hidden page that contains the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     The outline should include instructions for creating a basic web form with SQL query vulnerabilities, along with tips for integrating a Jurassic-themed login page complete with park maps and dinosaur silhouettes.

2. *Medium – “Fossilized Database”*  
   - **Challenge Description:**  
     This challenge simulates a scenario where users must extract data from a dinosaur fossil database. The SQL injection vulnerability is not immediately apparent and requires union-based injection to enumerate the database schema.  
   - **What the User Must Do:**  
     The user must perform a union-based SQL injection to list table names and column data, then piece together fragmented data that form the flag (e.g., `FLAG...`).  
   - **Technical Implementation:**  
     Provide detailed steps for setting up a database with multiple tables and intentional injection points. The outline should emphasize clear instructions on how to use union queries, and reference Jurassic-themed data (e.g., fossil records, excavation logs).

3. *Hard – “Prehistoric Pulse”*  
   - **Challenge Description:**  
     In this scenario, the SQL injection vulnerability is hidden behind a time-based blind SQL injection mechanism. The challenge is set in a prehistoric data center where timing differences are the only clue.  
   - **What the User Must Do:**  
     The user must use time delays in SQL queries to extract information one bit at a time. They must infer the flag (e.g., `FLAG...`) by analyzing the response delays and reconstructing the hidden string.  
   - **Technical Implementation:**  
     The outline should detail how to create a backend with blind SQL injection vulnerabilities, including instructions for simulating time delays. It should also incorporate Jurassic aesthetics—such as an interface resembling an ancient, crumbling data archive.

4. *Impossible – “Cretaceous Conundrum”*  
   - **Challenge Description:**  
     The ultimate SQL injection challenge combines multiple advanced techniques. The vulnerable application employs out-of-band injection and second-order SQL injection methods. The flag is obfuscated in a multi-step process within an intricately designed dinosaur research database.  
   - **What the User Must Do:**  
     The user must identify the initial injection point, exploit out-of-band channels to retrieve intermediate data, and then perform a second-order injection to reveal the final, encrypted flag (e.g., `FLAG...`). This challenge requires a deep understanding of database behavior and advanced SQL injection techniques.  
   - **Technical Implementation:**  
     The outline should include a comprehensive list of the necessary SQL commands, the design of a multi-layered database schema, and instructions for simulating out-of-band communication. Emphasize integration with a Jurassic-themed dashboard, complete with interactive dinosaur exhibit panels and animated prehistoric graphics.

----------------------------------------
Your goal is to produce an outline that is creative, technically detailed, and immersive. Each section of your outline must:
- Incorporate the user’s selected `[challenge_category]` and `[difficulty_level]`.
- Leverage additional context from `[additional_info]` when provided.
- Clearly delineate between the narrative (challenge description) and the technical blueprint (implementation steps).
- Reflect a rich, Jurassic World–themed experience throughout every element.

By following this template and including these detailed examples, you will provide a robust blueprint that guides subsequent steps in generating fully functional CTF output files—challenge instructions and setup instructions—and ultimately deliver an engaging, multi-modal, and thematic CTF challenge experience.""")

  response = model.invoke(prompt.invoke({
    "category": command.category.value, 
    "difficulty": command.difficulty.value,
    "additional_prompt": command.additional_prompt
  }))

  return response.content

async def create_challenge_output(outline: str) -> ChallengeOuptut:
  model = ChatOpenAI(model="o3-mini-2025-01-31", api_key=global_settings.OPENAI_API_KEY, max_completion_tokens=4096)
  structured_model = model.with_structured_output(ChallengeOuptut)

  response = structured_model.invoke(outline)

  return response