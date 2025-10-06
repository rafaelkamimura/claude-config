# Merge Request Draft Generator

Generates comprehensive merge request documentation in PT-BR compliance, analyzing commits and changes to create professional MR descriptions.

## Purpose
- Analyze branch commits and changes
- Generate detailed MR documentation in Portuguese (PT-BR)
- Extract technical details from git history
- Create structured, review-ready merge requests
- Never mention AI/automation tools

## Workflow

### Phase 1: Branch Analysis
1. **Get Current Branch**
   ```bash
   current_branch=$(git branch --show-current)
   ```
   - If not on a branch: STOP → "Not on a branch. Please checkout your feature branch first."

2. **Identify Base Branch**
   ```bash
   # Try to find merge base with common branches
   for base in main master develop development staging; do
     if git rev-parse --verify $base >/dev/null 2>&1; then
       merge_base=$(git merge-base HEAD $base 2>/dev/null)
       [ -n "$merge_base" ] && base_branch=$base && break
     fi
   done
   ```
   - If no base found: STOP → "What is the target branch for this MR? (main/master/develop):"

3. **Extract Task Context**
   ```bash
   # Check for task history
   task_file=$(ls -t .claude/task-history/*.md 2>/dev/null | head -1)
   ```
   - Parse task for objective and context

### Phase 2: Commit Analysis
1. **Get Commit List**
   ```bash
   # Get all commits from branch divergence
   git log --oneline $base_branch..HEAD
   ```

2. **Analyze Each Commit**
   ```bash
   # Get detailed commit info
   git log --format="%H|%s|%b|%an|%ad" --date=short $base_branch..HEAD
   ```
   - Extract commit hash, subject, body, author, date
   - Categorize by type (feat, fix, chore, docs, etc.)

3. **Get Commit Statistics**
   ```bash
   # For each commit
   git show --stat --format="" $commit_hash
   ```
   - Files changed
   - Lines added/removed

### Phase 3: File Change Analysis
1. **Overall Statistics**
   ```bash
   # Total diff statistics
   git diff --stat $base_branch..HEAD
   ```
   - Total files modified/created/deleted
   - Total insertions and deletions

2. **Detailed File Changes**
   ```bash
   # List all changed files with status
   git diff --name-status $base_branch..HEAD
   ```
   - A: Added files
   - M: Modified files
   - D: Deleted files
   - R: Renamed files

3. **Analyze Change Content**
   Use Task agents to analyze:
   - **backend-architect**: Architecture impacts
   - **code-reviewer**: Code quality aspects
   - **test-automator**: Test coverage
   - **database-optimizer**: Database changes
   - **security-auditor**: Security implications

### Phase 4: MR Content Generation
1. **Generate PT-BR Content Structure**
   ```markdown
   # Merge Request #[number]: [Título Descritivo]
   
   ## Objetivo
   [Descrição clara do objetivo da MR]
   
   ## Resumo das Alterações
   - **[N] arquivos modificados/criados**
   - **[N] inserções (+)**
   - **[N] deleções (-)**
   - **[N] commits totais**
   - **[Principais funcionalidades/correções]**
   
   ## Commits Incluídos
   [Lista numerada de commits com hash e mensagem]
   
   ## Funcionalidades Implementadas
   
   ### 1. [Funcionalidade Principal]
   [Descrição detalhada]
   
   #### Características Técnicas
   [Detalhes técnicos]
   
   ### 2. [Segunda Funcionalidade]
   [Descrição]
   
   ## Arquitetura Implementada
   [Se aplicável, diagramas ou descrições de arquitetura]
   
   ## Arquivos Criados/Modificados
   
   ### [Categoria 1]
   1. **path/to/file.ext** ([N] linhas)
      - [Descrição da mudança]
   
   ## Validações e Testes
   
   ### Testes Implementados
   - [Lista de testes adicionados]
   
   ### Cobertura
   - [Informações sobre cobertura de testes]
   
   ## Como Testar
   ```bash
   # Comandos para testar a funcionalidade
   ```
   
   ## Impacto e Riscos
   - **Impacto**: [Baixo/Médio/Alto] - [Justificativa]
   - **Riscos**: [Descrição dos riscos]
   - **Mitigação**: [Como os riscos foram mitigados]
   
   ## Checklist de Review
   - [ ] Código segue padrões do projeto
   - [ ] Nomenclatura consistente
   - [ ] Testes implementados
   - [ ] Documentação atualizada
   - [ ] Sem quebras de compatibilidade
   - [ ] Performance aceitável
   - [ ] Segurança verificada
   
   ## Próximos Passos Sugeridos
   [Lista de melhorias ou trabalhos futuros]
   
   ## Conclusão
   [Resumo final do que a MR adiciona ao projeto]
   ```

2. **PT-BR Terminology Mapping**
   - feature → funcionalidade
   - bug fix → correção de bug
   - improvement → melhoria
   - performance → desempenho
   - security → segurança
   - database → banco de dados
   - cache → cache (mantém)
   - endpoint → endpoint (mantém)
   - request/response → requisição/resposta
   - merge request → merge request (mantém)
   - commit → commit (mantém)
   - branch → branch (mantém)

3. **Technical Analysis Sections**
   Based on changes detected, include relevant sections:
   
   **For API Changes:**
   - Endpoints criados/modificados
   - Schemas de request/response
   - Validações implementadas
   - Documentação OpenAPI
   
   **For Database Changes:**
   - Migrações executadas
   - Tabelas criadas/modificadas
   - Índices adicionados
   - Queries otimizadas
   
   **For Infrastructure:**
   - Configurações Docker
   - Variáveis de ambiente
   - Serviços adicionados
   - Dependências atualizadas

### Phase 5: Review and Output
1. **Clean Content**
   Remove any references to:
   - Claude, AI, agents, automation
   - Generated content markers
   - Task-init system references

2. **Present Draft**
   ```markdown
   ## Merge Request Draft Generated
   
   File saved to: .claude/mr-drafts/[timestamp]-[branch].md
   
   Preview:
   [First 50 lines of MR content]
   ```

3. **STOP** → "Review MR draft. Options: (edit/save/copy/discard):"
   - edit: Open in editor
   - save: Keep as-is
   - copy: Copy to clipboard
   - discard: Delete draft

4. **Save Final Version**
   ```bash
   # Save to project
   mkdir -p .claude/mr-drafts
   cat > .claude/mr-drafts/[timestamp]-[branch].md
   
   # Update gitignore
   grep -q "^.claude/mr-drafts/" .gitignore || echo ".claude/mr-drafts/" >> .gitignore
   ```

## Smart Detection Features

### Functionality Detection
Automatically identifies:
- **API Endpoints**: Routes, controllers, handlers
- **Database Changes**: Migrations, models, queries
- **Frontend Components**: React/Vue/Angular components
- **Tests**: Unit, integration, E2E tests
- **Configuration**: Environment, Docker, CI/CD
- **Documentation**: README, API docs, comments

### Impact Assessment
Calculates impact based on:
- Number of files changed
- Critical path modifications
- Database schema changes
- API contract changes
- Configuration updates

### Risk Analysis
Identifies risks from:
- Large file changes (>500 lines)
- Database migrations
- Security-related files
- Authentication/authorization changes
- External service integrations

## Integration with Workflow

### Command Flow
```
/task-init → development → /commit → /mr-draft → push → create MR
```

### Task Context
- Reads from `.claude/task-history/`
- Links MR to original task objective
- Includes success criteria in validation

### Commit History
- Uses commits from `/commit` command
- Maintains clean history narrative
- Groups related changes logically

## PT-BR Compliance Rules

### Language Standards
1. **Technical Terms**: Keep English where standard
   - API, REST, HTTP, JSON, etc.
   - Framework names (React, Django, etc.)
   - Git terminology (commit, branch, merge)

2. **Translate Common Terms**:
   - added → adicionado
   - removed → removido
   - updated → atualizado
   - fixed → corrigido
   - improved → melhorado
   - created → criado
   - deleted → deletado/removido

3. **Section Headers in Portuguese**:
   - Objetivo (Purpose)
   - Resumo (Summary)
   - Funcionalidades (Features)
   - Arquivos (Files)
   - Testes (Tests)
   - Riscos (Risks)
   - Conclusão (Conclusion)

### Formatting Standards
- Use Brazilian number format (1.234,56)
- Date format: DD/MM/YYYY
- Time format: HH:mm:ss
- Maintain formal tone ("foi implementado" not "implementamos")

## Error Handling

### No Commits
- Check if branch has commits
- Suggest checking branch or committing changes

### Merge Conflicts
- Detect if branch has conflicts with base
- Warn about need to resolve before MR

### Large MRs
- Warn if >20 files or >1000 lines changed
- Suggest breaking into smaller MRs

### Missing Tests
- Flag if no test files detected
- Remind about test requirements

## Advanced Features

### Template Customization
Check for project-specific template:
```bash
if [ -f .claude/mr-template.md ]; then
  # Use custom template
fi
```

### Auto-Detection
- Project type from files (package.json, pom.xml, etc.)
- Framework from imports/dependencies
- Testing framework from test files
- CI/CD from workflow files

### Statistics Generation
- Lines of code by language
- Test coverage delta (if available)
- Performance metrics (if measured)
- Security scan results (if available)

## Output Options

### File Output
Default: `.claude/mr-drafts/[timestamp]-[branch].md`

### Clipboard Copy
Option to copy directly for pasting into GitLab/GitHub

### Direct Integration
Future: Direct MR creation via API:
- GitLab API
- GitHub API
- Bitbucket API

## Best Practices

1. **One Feature Per MR**
   - Keep MRs focused and reviewable
   - Easier to track and rollback

2. **Clear Objectives**
   - State the problem being solved
   - Explain the solution approach

3. **Comprehensive Testing**
   - Document test scenarios
   - Include test commands

4. **Risk Assessment**
   - Be transparent about impacts
   - Provide mitigation strategies

5. **Review Readiness**
   - Complete checklist items
   - Ensure CI/CD passes

## Notes
- MR drafts are project-specific
- Never mentions AI assistance
- Maintains professional PT-BR tone
- Focuses on technical accuracy
- Provides actionable review guidance