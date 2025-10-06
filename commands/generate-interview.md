# /generate-interview Command

Custom Claude Code command for generating tailored interview questions based on candidate resumes.

## Usage

```
/generate-interview [/path/to/resume]

[candidate name]
[role]
[seniority level]

[optional extra context]
```

## Required Parameters
- **Resume path**: Path to candidate's PDF resume
- **Candidate name**: Full name of the candidate
- **Role**: Position they're applying for (e.g., Mobile Developer, Backend Engineer, Full Stack Developer)
- **Seniority level**: Junior, Mid-level (Pleno), Senior, Lead, Principal

## Optional Parameters
- **Extra context**: Additional information about the position, team needs, or specific skills to evaluate

## Command Pipeline

### Step 1: Input Validation
- Validate all required parameters are provided
- Check if resume file exists
- Prompt for missing required fields

### Step 2: Directory Setup
- Create candidate directory at `/Users/nagawa/v2t/interview-generator/[candidate-name]`
- Move original resume to candidate directory
- Convert PDF to markdown for analysis

### Step 3: Resume Analysis
- Analyze candidate's experience, skills, and background
- Identify strong points and areas to probe
- Generate bilingual analysis (English for internal use and Portuguese for team)
- Present summary and confirm with user

### Step 4: Interview Configuration
- Prompt for interview type:
  - A) Chat-like conversation
  - B) Live coding session
  - C) Chat with code review
  - D) Combination of above
- Prompt for interview duration:
  - A) 15 minutes (quick screening)
  - B) 30 minutes (standard)
  - C) Custom duration

### Step 5: Question Generation
- Generate customized questions in Portuguese (ptBR)
- Keep technical terms, technologies, and code in English
- Base questions on:
  - Resume analysis
  - Role requirements
  - Seniority expectations
  - Interview type and duration
- Include evaluation scorecard
- Add interviewer notes and tips

### Step 6: Context Storage
- Save interview context to `~/.claude/interviews-nlp`
- Store analysis patterns for future interviews
- Build knowledge base of role-specific questions

## Output Structure

```
/Users/nagawa/v2t/interview-generator/
└── [candidate-name]/
    ├── resume.pdf (original)
    ├── resume.md (converted)
    ├── analysis.md (English - internal use)
    ├── analysis_ptbr.md (Portuguese - for team)
    └── interview_questions_ptbr.md (Portuguese questions with English tech terms)
```

## Command Implementation

When this command is invoked, Claude Code will:

1. **Parse Input**: Extract parameters from user input
2. **Validate**: Ensure all required fields are present
3. **Setup**: Create directory structure and move files
4. **Convert**: Transform PDF to markdown using appropriate tools
5. **Analyze**: Perform deep analysis of candidate's background
6. **Interact**: Get user confirmation and preferences
7. **Generate**: Create tailored interview questions in ptBR
8. **Store**: Save context for future use

## Analysis Framework

### Strong Points to Identify:
- Relevant direct experience
- Technology stack matches
- Project complexity and scale
- Leadership or mentoring experience
- Educational background
- Certifications and training
- Open source contributions

### Areas to Probe:
- Technology gaps vs job requirements
- Depth vs breadth of experience
- Practical vs theoretical knowledge
- Problem-solving approach
- Communication skills
- Cultural fit indicators
- Growth potential

## Interview Question Format (ptBR)

### Exemplo de Estrutura:

```markdown
# Entrevista Técnica - [Nome do Candidato]
## Posição: [Cargo] [Nível]

### AQUECIMENTO (X minutos)
"Oi [Nome], obrigado por participar. Vi que você [contexto do currículo].
Pode me contar sobre [experiência relevante]?"

### SEÇÃO 1: AVALIAÇÃO TÉCNICA
**P1:** "Você trabalhou com [technology]. Como você lidaria com [scenario]?"
*Observar: [evaluation criteria]*

**P2:** "Me explica a diferença entre [concept A] e [concept B] no contexto de [framework]?"
*Esperado: Understanding of [technical concepts]*

### Code Review
"Aqui tem um componente React Native. Quais problemas você identifica?"
```javascript
// Code sample in English
const Component = () => {
  // ...
}
```

### SCORECARD DE AVALIAÇÃO
- **Conhecimento de [Tech]:** ⚪ Fraco ⚪ Adequado ⚪ Forte
- **Problem Solving:** ⚪ Fraco ⚪ Adequado ⚪ Forte
```

## Interview Types

### A) Conversa Estilo Chat
- Discussão de experiências
- Questões comportamentais
- Cenários de problem-solving
- Avaliação de fit cultural

### B) Live Coding
- Desafios de algoritmos
- Implementação de features
- Exercícios de debugging
- Code optimization

### C) Chat com Code Review
- Review de código anterior do candidato
- Discussão de design decisions
- Arquitetura e patterns
- Best practices

## Context Storage Format

Context is stored in natural language at `~/.claude/interviews-nlp/[timestamp]-[candidate].txt`:

```
Interview Context for [Candidate Name]
Date: [Date]
Role: [Role]
Seniority: [Level]

Key Strengths Identified:
- [Strength 1]
- [Strength 2]

Areas Assessed:
- [Area 1]
- [Area 2]

Question Patterns Used:
- [Pattern 1]
- [Pattern 2]

Interview Outcome: [If known]
Notes for Future: [Learnings]
```

## Example Execution

```
User: /generate-interview /Users/downloads/maria_silva_resume.pdf

Maria Silva
Mobile Developer
Pleno

Experiência com Flutter mas precisamos de alguém que também trabalhe com React Native

Claude:
1. ✅ Criando diretório para Maria Silva...
2. ✅ Movendo e convertendo currículo...
3. 🔍 Analisando currículo...

[Resumo da Análise]
Pontos Fortes:
- 2 anos de experiência com Flutter
- Apps publicados na Play Store
- Conhecimento de Dart e Firebase

Áreas para Explorar:
- Experiência com React Native
- State management
- Performance optimization

Prosseguir com esta análise? (s/n)

[Após confirmação]

Selecione o tipo de entrevista:
A) Conversa estilo chat
B) Live coding
C) Chat com code review
D) Combinação

Selecione a duração:
A) 15 minutos
B) 30 minutos
C) Personalizada

[Gera perguntas customizadas em português]
```

## Template Examples from Existing Interviews

The command leverages patterns from:
- `/Users/nagawa/Downloads/entrevistas/lucas_germano/` - Mobile Developer questions
- `/Users/nagawa/Downloads/entrevistas/sei la/artur_quick_screening.md` - Quick screening format
- `/Users/nagawa/Downloads/entrevistas/pedro_porto/` - Junior developer assessment

## Question Language Guidelines

### Keep in English:
- Technology names (React Native, Flutter, Swift, etc.)
- Technical concepts (state management, props, hooks, etc.)
- Code snippets and examples
- Framework-specific terms
- Design patterns (MVC, MVVM, etc.)

### Translate to Portuguese:
- Question prompts
- Instructions
- Evaluation criteria
- Behavioral questions
- Context descriptions
- Scorecard labels

## Best Practices

1. **Adequar ao Nível**: Match questions to seniority (Júnior/Pleno/Sênior)
2. **Usar Exemplos Concretos**: Reference specific resume items
3. **Balancear Cobertura**: Mix technical, behavioral, and cultural fit
4. **Gerenciamento de Tempo**: Clear time allocations
5. **Feedback Acionável**: Include clear evaluation criteria

## Error Handling

- Missing resume file: Prompt for valid path
- Invalid PDF: Attempt alternative conversion methods
- Missing parameters: Interactive prompts for required fields
- Conversion failure: Fallback to manual analysis request

## Integration Points

- Existing interview templates in `/Users/nagawa/Downloads/entrevistas/`
- Previous candidate assessments for pattern learning
- Context storage for continuous improvement
- Team feedback integration

## Future Enhancements

- Auto-detect seniority from resume
- Technology stack matching score
- Difficulty calibration based on role
- Interview performance tracking
- Team-specific question banks
- Multi-language support expansion