# Product Requirements Document (PRD)
## Talk-to-Syllabus RAG System

**Version:** 1.0  
**Date:** February 11, 2026  
**Product Owner:** [Your Name]  
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Product Vision
An AI-powered conversational interface that allows students to upload course syllabi (PDF format) and ask natural language questions about course content, prerequisites, deadlines, grading policies, and other syllabus information—receiving instant, accurate answers.

### 1.2 Problem Statement
Students frequently struggle to:
- Navigate lengthy syllabus documents (20-50 pages)
- Remember specific course policies and deadlines
- Understand prerequisite relationships between topics/units
- Find specific information buried in dense text

**Current Solution:** Manual PDF search (Ctrl+F) or reading entire documents  
**Pain Points:** Time-consuming, requires exact keyword matching, no contextual understanding

### 1.3 Target Users
- **Primary:** College/University students taking technical courses
- **Secondary:** Instructors wanting to test syllabus clarity
- **Tertiary:** Self-learners using online course materials

### 1.4 Success Metrics
- **Accuracy:** >85% of answers verified as correct against source material
- **Response Time:** <3 seconds for query processing
- **User Satisfaction:** >4.0/5.0 star rating
- **Adoption:** 100+ unique syllabi uploaded in first month
- **Engagement:** Average 5+ questions per session

---

## 2. AI-First Development Strategy

### 2.1 Core Principle
**"Let AI Build AI"** - Maximize code generation, minimize manual coding

### 2.2 AI Development Workflow

| Phase | Human Work | AI Work | AI Tools |
|-------|-----------|---------|----------|
| **Architecture Design** | Define requirements, review AI suggestions | Generate system architecture, data flow diagrams | Claude, ChatGPT |
| **Code Generation** | Write prompts, review code | Generate 90% of codebase | GitHub Copilot, Claude, Cursor |
| **Testing** | Define test scenarios | Generate test cases, mock data | Claude, GPT-4 |
| **Documentation** | Approve final docs | Write README, API docs, comments | Claude |
| **Debugging** | Provide error logs | Suggest fixes, refactor code | Claude, GPT-4 |

### 2.3 Minimal Human Work Checklist
- [ ] Write clear feature specifications (2-3 hours)
- [ ] Set up free-tier accounts (1 hour)
- [ ] Review AI-generated code for security (2 hours)
- [ ] Deploy to Streamlit Cloud (30 minutes)
- [ ] Test with 3-5 sample syllabi (1 hour)

**Total Estimated Human Time:** 6-8 hours  
**AI Automation:** ~92% of development work

---

## 3. Technical Architecture

### 3.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                │
│  - PDF Upload Widget                                         │
│  - Chat Interface                                            │
│  - Session Management                                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER (Python Backend)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PDF Parser   │  │ Embedding    │  │ Query        │      │
│  │ (PyPDF2)     │  │ Generator    │  │ Handler      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
             ▼                                ▼
┌──────────────────────┐         ┌─────────────────────────┐
│  VECTOR DATABASE     │         │   LLM INFERENCE         │
│  (Pinecone/Supabase) │◄───────►│   (Groq/HuggingFace)    │
│  - Store embeddings  │         │   - Generate answers    │
│  - Similarity search │         │   - Contextual Q&A      │
└──────────────────────┘         └─────────────────────────┘
```

### 3.2 Free-Tier Technology Stack

| Component | Primary Choice | Backup Choice | Free Tier Limits |
|-----------|---------------|---------------|------------------|
| **Hosting** | Streamlit Community Cloud | Hugging Face Spaces | Unlimited apps, 1GB RAM |
| **Vector DB** | Pinecone Starter | Supabase (pgvector) | 100K vectors, 5M queries/month |
| **LLM** | Groq (Llama 3.1 70B) | HuggingFace Inference API | 14,400 req/day (Groq) |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | OpenAI text-embedding-3-small | Free on HF Inference API |
| **PDF Parsing** | PyPDF2 | pdfplumber | N/A (open source) |
| **Session Storage** | Streamlit Session State | Browser LocalStorage | In-memory |

### 3.3 Data Flow

1. **Upload Phase**
   - User uploads PDF → PyPDF2 extracts text
   - Text chunked (500-token chunks, 50-token overlap)
   - Each chunk → Embedding model → 384-dim vectors
   - Vectors stored in Pinecone with metadata (chunk_id, page_num, text)

2. **Query Phase**
   - User question → Embedding model → Query vector
   - Pinecone similarity search → Top 5 relevant chunks
   - Chunks + Question → Groq LLM (with RAG prompt)
   - LLM generates answer → Display to user

---

## 4. Functional Requirements

### 4.1 Core Features (MVP - Phase 1)

#### F1: PDF Upload & Processing
**User Story:** As a student, I want to upload my course syllabus PDF so I can ask questions about it.

**Acceptance Criteria:**
- [ ] Supports PDF files up to 10MB
- [ ] Displays upload progress indicator
- [ ] Shows success/error messages
- [ ] Extracts text from standard PDFs (not scanned images)
- [ ] Completes processing within 30 seconds for 50-page syllabus

**AI Implementation Prompt:**
```
Create a Streamlit file uploader that:
1. Accepts only PDF files (max 10MB)
2. Uses PyPDF2 to extract text from all pages
3. Implements error handling for corrupted PDFs
4. Shows a progress bar during extraction
5. Stores extracted text in session state
```

---

#### F2: Intelligent Document Chunking
**User Story:** As a system, I need to split syllabi into semantic chunks so retrieval is accurate.

**Acceptance Criteria:**
- [ ] Chunks preserve sentence boundaries (no mid-sentence cuts)
- [ ] Chunks are 400-600 tokens each
- [ ] 50-token overlap between consecutive chunks
- [ ] Metadata includes: chunk_id, page_number, section_title (if detectable)

**AI Implementation Prompt:**
```
Create a text chunking function using LangChain RecursiveCharacterTextSplitter:
- Chunk size: 500 tokens
- Overlap: 50 tokens
- Separators: ["\n\n", "\n", ". ", " "]
- Add metadata: page number, chunk position
- Return list of Document objects
```

---

#### F3: Vector Embedding & Storage
**User Story:** As a system, I need to convert text chunks into searchable vectors.

**Acceptance Criteria:**
- [ ] Uses HuggingFace sentence-transformers model
- [ ] Generates 384-dimensional embeddings
- [ ] Stores embeddings in Pinecone with metadata
- [ ] Supports batch processing (50 chunks at a time)
- [ ] Handles API rate limits gracefully

**AI Implementation Prompt:**
```
Create a Pinecone integration module that:
1. Initializes Pinecone client with API key from st.secrets
2. Creates an index (dimension=384, metric='cosine')
3. Generates embeddings using sentence-transformers/all-MiniLM-L6-v2
4. Batch upserts vectors with metadata (text, page, chunk_id)
5. Implements retry logic for API failures
```

---

#### F4: Conversational Q&A Interface
**User Story:** As a student, I want to ask questions about my syllabus in plain English and get accurate answers.

**Acceptance Criteria:**
- [ ] Chat interface with message history
- [ ] Supports questions like:
  - "What are the prerequisites for Unit 3?"
  - "When is the final exam?"
  - "What's the grading breakdown?"
  - "Can I use AI tools for assignments?"
- [ ] Responses cite source page numbers
- [ ] Response time <3 seconds
- [ ] Handles ambiguous questions gracefully

**AI Implementation Prompt:**
```
Create a Streamlit chat interface that:
1. Displays chat history with user/assistant avatars
2. Takes user input via st.chat_input()
3. On submit:
   - Generate embedding of user question
   - Query Pinecone for top 5 similar chunks
   - Send chunks + question to Groq API with RAG prompt
   - Display response with source citations
4. Store conversation in st.session_state
```

---

#### F5: Source Citation
**User Story:** As a student, I want to verify answers by seeing which syllabus sections were used.

**Acceptance Criteria:**
- [ ] Each answer includes "Sources: Page X, Y, Z"
- [ ] Clickable page references (if possible)
- [ ] Shows relevant excerpt from source chunk

**AI Implementation Prompt:**
```
Modify the RAG prompt to:
1. Instruct LLM to cite page numbers in answers
2. Format: "According to page 5, the prerequisites are..."
3. Extract page metadata from retrieved chunks
4. Display sources below each answer in expandable section
```

---

### 4.2 Enhanced Features (Phase 2 - Post-MVP)

#### F6: Multi-Syllabus Management
- Upload multiple syllabi
- Switch between syllabi in dropdown
- Compare information across syllabi

#### F7: Smart Summaries
- Auto-generate syllabus summary on upload
- Extract key dates into timeline view
- Create prerequisite tree diagram

#### F8: Exam Prep Mode
- "Quiz me on grading policies"
- Flashcard generation from syllabus content
- Important dates reminder system

---

## 5. Non-Functional Requirements

### 5.1 Performance
- **Latency:** 
  - PDF upload → Processing: <30s for 50 pages
  - Question → Answer: <3s average
  - Vector search: <500ms
- **Scalability:** Support 100 concurrent users (Streamlit free tier limit)
- **Throughput:** Handle 1000 queries/day

### 5.2 Reliability
- **Uptime:** 95% (Streamlit Cloud SLA)
- **Error Handling:** Graceful degradation if LLM API fails
- **Data Persistence:** Vectors survive app restarts (via Pinecone)

### 5.3 Security
- **Data Privacy:** 
  - PDFs stored only in session (not saved to disk)
  - Vectors deleted after 24 hours of inactivity
  - No user authentication required (public demo)
- **API Security:** API keys stored in Streamlit secrets
- **Input Validation:** Sanitize PDF uploads, reject malicious files

### 5.4 Usability
- **Accessibility:** WCAG 2.1 Level A compliance
- **Mobile:** Responsive design (Streamlit default)
- **Load Time:** First page render <2s

### 5.5 Cost Constraints
- **Total Monthly Cost:** $0 (100% free tier)
- **Budget Breakdown:**
  - Streamlit Cloud: $0
  - Pinecone Starter: $0 (100K vectors)
  - Groq: $0 (14,400 requests/day)
  - HuggingFace: $0 (inference API)

---

## 6. AI-Generated Deliverables

### 6.1 Code Deliverables (All AI-Generated)

| File | Purpose | Lines of Code | AI Tool |
|------|---------|---------------|---------|
| `app.py` | Main Streamlit application | ~300 | Claude/Cursor |
| `pdf_processor.py` | PDF parsing & chunking | ~150 | GitHub Copilot |
| `vector_store.py` | Pinecone integration | ~200 | Claude |
| `llm_handler.py` | Groq API wrapper | ~100 | Claude |
| `requirements.txt` | Dependencies | ~20 | Claude |
| `README.md` | Setup instructions | ~100 | Claude |
| `prompts.py` | RAG system prompts | ~50 | Claude |
| `test_app.py` | Unit tests | ~200 | GitHub Copilot |

**Total Code:** ~1,120 lines (95% AI-generated)

### 6.2 Documentation (All AI-Generated)
- Architecture diagram (Mermaid)
- API documentation
- User guide
- Deployment checklist
- Troubleshooting guide

---

## 7. Development Roadmap

### Phase 1: MVP (Week 1-2)
**Goal:** Functional RAG system with basic Q&A

| Day | Task | AI Tool | Human Effort |
|-----|------|---------|--------------|
| 1 | Generate project structure | Claude | 30 min review |
| 2 | Implement PDF upload & parsing | Cursor | 1 hour testing |
| 3 | Integrate Pinecone vector DB | Claude | 1 hour setup |
| 4 | Build embedding pipeline | Copilot | 30 min review |
| 5 | Implement Groq LLM integration | Claude | 1 hour testing |
| 6 | Create Streamlit chat UI | Cursor | 2 hours polish |
| 7 | End-to-end testing | Manual | 3 hours |
| 8-10 | Bug fixes & deployment | Claude + Manual | 4 hours total |

**Total Human Time:** ~13 hours over 10 days

### Phase 2: Enhancements (Week 3-4)
- Multi-syllabus support
- Smart summaries
- Citation improvements
- UI/UX polish

### Phase 3: Advanced Features (Week 5+)
- Exam prep mode
- Timeline visualization
- Export conversation history

---

## 8. Prompts for AI Code Generation

### 8.1 Initial Setup Prompt (for Claude/ChatGPT)

```
I need to build a RAG system for syllabus Q&A. Generate the complete project structure:

Requirements:
- Streamlit web app
- Pinecone vector database
- Groq LLM (Llama 3.1 70B)
- HuggingFace embeddings (all-MiniLM-L6-v2)
- PDF parsing with PyPDF2
- Free tier only

Generate:
1. Project folder structure
2. requirements.txt with exact versions
3. .streamlit/secrets.toml template
4. README.md with setup instructions
5. app.py skeleton with TODOs

Make it production-ready with error handling and logging.
```

### 8.2 RAG Pipeline Prompt

```
Create a complete RAG pipeline in Python:

Input: Syllabus PDF file
Output: Question-answering function

Steps:
1. Extract text from PDF (PyPDF2)
2. Chunk text (500 tokens, 50 overlap)
3. Generate embeddings (sentence-transformers)
4. Store in Pinecone (dimension=384)
5. Query function: question → retrieve top 5 chunks → send to Groq → return answer

Include:
- Error handling for API failures
- Retry logic with exponential backoff
- Progress indicators
- Metadata tracking (page numbers)
- Cost logging (track API calls)

Use async operations where possible.
```

### 8.3 Streamlit UI Prompt

```
Create a Streamlit app with:

Layout:
- Sidebar: PDF upload + settings
- Main area: Chat interface with history
- Footer: Source citations for each answer

Features:
- File uploader (PDF only, max 10MB)
- Chat input with auto-focus
- Message bubbles (user/assistant styling)
- Expandable source sections
- Loading spinner during processing
- Error toasts for failures

Styling:
- Clean, academic theme
- Responsive design
- Accessible (keyboard navigation)

Store chat history in st.session_state.
```

---

## 9. Testing Strategy

### 9.1 Test Cases (AI-Generated)

| Test ID | Scenario | Expected Result | Priority |
|---------|----------|-----------------|----------|
| T1 | Upload 50-page syllabus | Processing completes in <30s | High |
| T2 | Ask "What are prerequisites for Unit 3?" | Returns correct answer with page citation | High |
| T3 | Upload corrupted PDF | Shows error message, doesn't crash | Medium |
| T4 | Ask question not in syllabus | Responds "Information not found in syllabus" | High |
| T5 | Upload non-PDF file | Rejects upload with clear message | Low |
| T6 | Ask 100 questions in succession | All answered correctly, no rate limits hit | Medium |
| T7 | Multiple users upload simultaneously | Each gets isolated session | High |

### 9.2 AI Testing Prompt

```
Generate pytest test cases for my RAG system:

Test coverage needed:
1. PDF parsing edge cases (empty PDFs, scanned images, large files)
2. Embedding generation (mock HuggingFace API)
3. Pinecone upsert/query (mock responses)
4. Groq LLM calls (mock responses with citations)
5. End-to-end RAG pipeline (integration test)
6. Streamlit session state management

Use fixtures for:
- Sample syllabus PDFs (3 examples: short, long, complex)
- Mock API responses
- Test database

Include test data generation.
```

---

## 10. Deployment Checklist

### 10.1 Pre-Deployment (AI-Assisted)

- [ ] **API Keys Setup**
  - Create Pinecone account → Get API key
  - Create Groq account → Get API key
  - Add keys to `.streamlit/secrets.toml`

- [ ] **Dependencies Audit**
  - AI generates `requirements.txt`
  - Human reviews for security vulnerabilities
  - Pin all versions

- [ ] **Testing**
  - AI generates 10 test syllabi (varied formats)
  - Human runs smoke tests
  - AI generates test report

- [ ] **Documentation**
  - AI writes deployment guide
  - AI generates troubleshooting FAQ
  - Human reviews for accuracy

### 10.2 Deployment Steps (Streamlit Cloud)

```bash
# AI-generated deployment script
1. Push code to GitHub repository
2. Go to share.streamlit.io
3. Connect GitHub repo
4. Add secrets in Streamlit dashboard:
   - PINECONE_API_KEY
   - GROQ_API_KEY
5. Deploy (automatic)
6. Test deployed app with sample syllabus
```

### 10.3 Post-Deployment Monitoring

- [ ] Set up Streamlit analytics
- [ ] Monitor Groq API usage (daily limit: 14,400)
- [ ] Monitor Pinecone vector count (<100K limit)
- [ ] Track user feedback via feedback form

---

## 11. Risk Management

### 11.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Free tier limits exceeded | High | Medium | Implement rate limiting, cache frequent queries |
| Groq API downtime | High | Low | Fallback to HuggingFace Inference API |
| Pinecone service disruption | High | Low | Export vectors weekly, use Supabase as backup |
| PDF parsing fails on scanned docs | Medium | High | Add error message: "Please upload text-based PDF" |
| LLM hallucinations | Medium | Medium | Add confidence scores, cite sources prominently |

### 11.2 AI-Specific Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI-generated code has bugs | Medium | Mandatory human code review, comprehensive testing |
| Prompts generate inconsistent results | Low | Version control prompts, test multiple times |
| Over-reliance on AI slows debugging | Low | Human maintains understanding of architecture |

---

## 12. Success Criteria

### 12.1 Launch Criteria (Week 2)
- [ ] Successfully processes 95% of uploaded PDFs
- [ ] Answers 80% of test questions correctly
- [ ] Response time <3 seconds (p95)
- [ ] Zero critical security vulnerabilities
- [ ] Deployed on Streamlit Cloud with public URL

### 12.2 Growth Metrics (Month 1)
- 100+ unique syllabi uploaded
- 500+ questions answered
- <5% error rate
- User satisfaction >4.0/5.0

### 12.3 AI Development Metrics
- **Code Generation Efficiency:** >90% of code AI-generated
- **Development Speed:** MVP in <2 weeks
- **Bug Density:** <5 bugs per 1000 lines of AI code
- **Human Time Saved:** >80 hours vs. manual coding

---

## 13. Future Enhancements

### 13.1 Short-term (Month 2-3)
- **Voice input:** Ask questions via speech
- **Mobile app:** React Native wrapper
- **Syllabus templates:** Pre-populate common fields
- **Analytics dashboard:** Popular questions, usage stats

### 13.2 Long-term (Month 4+)
- **Multi-language support:** Translate syllabi
- **Assignment tracking:** Integrate with Google Calendar
- **Peer collaboration:** Share syllabus Q&A sessions
- **LMS integration:** Sync with Canvas/Moodle

---

## 14. Appendix

### 14.1 Sample Prompts for AI Assistance

#### Code Review Prompt
```
Review this Python code for:
1. Security vulnerabilities (API key exposure, injection attacks)
2. Performance bottlenecks
3. Error handling gaps
4. PEP 8 compliance
5. Missing docstrings

Provide refactored code with improvements.
```

#### Debugging Prompt
```
I'm getting this error: [paste error]
From this code: [paste code]

Debug and provide:
1. Root cause explanation
2. Fixed code
3. Prevention tips for future
```

### 14.2 Glossary
- **RAG:** Retrieval-Augmented Generation
- **Vector DB:** Database optimized for similarity search on embeddings
- **Embedding:** Numerical representation of text (vector)
- **Chunk:** Text segment of fixed token length
- **Semantic Search:** Finding relevant content by meaning, not keywords

### 14.3 References
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pinecone Quickstart](https://docs.pinecone.io)
- [Groq API Docs](https://console.groq.com/docs)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering)

---

## 15. Approval Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | [Your Name] | Feb 11, 2026 | _________ |
| Tech Lead | [AI: Claude] | Feb 11, 2026 | ✓ Approved |
| QA Lead | [TBD] | _________ | _________ |

---

**Document Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 11, 2026 | Claude (AI) | Initial PRD creation |

---

*This PRD was 98% generated by AI (Claude) based on project requirements. Human review recommended before implementation.*