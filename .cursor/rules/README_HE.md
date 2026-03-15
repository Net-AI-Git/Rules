# תיעוד כללי Cursor — בעברית

זה המסמך בעברית לכל **Cursor Rules** בפרויקט. כאן תמצא: מה כל חוק אומר, **מתי להשתמש** בו, ואילו **ספריות וטכנולוגיות** הוא מגדיר. המטרה: שכל פעם שתרצה להבין איזה חוק רלוונטי עכשיו — זה יהיה ברור וקל לגשת.

**למחליטים (ראשי צוות, מפתחים חיצוניים):** תחת כל חוק בפירוט יש גם סעיף **"למחליט (האם לאמץ?)"** — הסבר קצר בשפה פשוטה: מה החוק נותן לקוד ולצוות, ומתי כדאי לאמץ אותו. עוזר להחליט אם להוסיף את הדרישות של החוק לפרויקט בלי להיכנס לפרטים הטכניים.

**פרטים טכניים** (מבנה תיקיות, frontmatter, סוגי הפעלה) — ראה [README.md](README.md) (באנגלית).

---

## טבלת גישה מהירה — "איזה חוק אני צריך עכשיו?"

| שם החוק | מתי להשתמש | סוג הפעלה | ספריות עיקריות |
|---------|-------------|-----------|-----------------|
| **core-python-standards** | כל משימת קוד Python | Always | asyncio, ProcessPoolExecutor, httpx, typing, Splunk (לוגים) |
| **error-handling-and-resilience** | טיפול בשגיאות, retry, circuit breaker | Always | Tenacity, circuitbreaker, Splunk |
| **security-governance-and-observability** | אבטחה, governance, OWASP LLM | Always | — |
| **audit-protocol** | ביקורות, compliance, audit trail | Always | Splunk, HEC |
| **final-review-protocol** | לפני שליחת תשובה סופית — בדיקת ציות | Always | pydantic-settings, pytest, Docker, FastAPI |
| **prompt-injection-prevention** | מניעת הזרקת פרומפטים, סניטציית קלט | לפי הקשר | — |
| **planner-strategic-planning** | תכנון אסטרטגי לפני פירוק משימות | לפי הקשר | LangGraph |
| **executor-action-translation** | תרגום תוכניות לאקשנים קונקרטיים | לפי הקשר | LangChain |
| **memory-and-archival-management** | זיכרון ארוך טווח, Vector DB, ארכיון | לפי הקשר | Vector DB, PostgreSQL, LangGraph |
| **multi-agent-systems** | ארכיטקטורת multi-agent (Orchestrator/Worker/Synthesizer) | לפי הקשר | LangGraph, asyncio.gather |
| **agentic-logic-and-tools** | יסודות LangChain, כלים, agent internals | לפי הקשר | LangChain, PydanticAI, LCEL |
| **contract-scope-and-boundaries** | מתי להגדיר חוזים מפורשים (ABC/Schema) | לפי הקשר | ABC, Pydantic, JSON Schema |
| **agent-component-interfaces** | חוזים בין Planner, Memory, Executor | לפי הקשר | abc.ABC, Pydantic |
| **cost-and-budget-management** | תקציב טוקנים ועלויות בזמן אמת | לפי הקשר | LangGraph (BudgetState) |
| **human-in-the-loop-approval** | סכמת Approval ל-HITL interrupts | לפי הקשר | LangGraph interrupts |
| **model-routing-and-selection** | ניתוב דינמי לפי מורכבות משימה | לפי הקשר | Splunk (מטריקות) |
| **reflection-and-self-critique** | Reviewer Node, self-critique לפני סינתזה | לפי הקשר | — |
| **data-schemas-and-interfaces** | סכמות Pydantic, מודלים מובנים | לפי הקשר | Pydantic BaseModel, Field |
| **configuration-and-dependency-injection** | קונפיגורציה והזרקת תלויות | לפי הקשר | pydantic-settings, SecretStr |
| **uvicorn-asgi-server** | הרצת אפליקציות ASGI (FastAPI) | לפי הקשר | Uvicorn, uvloop, httptools, watchfiles |
| **deployment-and-infrastructure** | CI/CD, Docker, Kubernetes | לפי הקשר | Docker, Kubernetes, Uvicorn, Trivy/Snyk, Splunk |
| **monitoring-and-observability** | מטריקות, לוגים, tracing | לפי הקשר | Splunk, HEC, SPL |
| **rate-limiting-and-queue-management** | rate limiting, תורים, multi-agent | לפי הקשר | FastAPI (middleware) |
| **performance-optimization** | קאשינג, אופטימיזציה, connection pooling | לפי הקשר | Redis, functools.lru_cache, CDN |
| **multi-tenancy-and-isolation** | בידוד tenant, אסטרטגיות DB | לפי הקשר | PostgreSQL (schema/row-level) |
| **code-review-and-collaboration** | code review, Git workflow | לפי הקשר | ruff, black, GitFlow |
| **versioning-and-release-management** | גרסאות סמנטיות, CHANGELOG | לפי הקשר | Keep a Changelog |
| **gitflow-branching-model** | מודל ענפים: master, develop, release, hotfix | לפי הקשר | Git |
| **llm-judge-protocol** | הערכת ביצועים/בטיחות/לוגיקה (LLM-as-Judge) | לפי הקשר | — |
| **mcp-protocol-implementation** | שרתים ולקוחות MCP לכלים דינמיים | לפי הקשר | MCP (mcp.server), JSON-RPC |
| **langgraph-architecture-and-nodes** | מבנה workflow, READ→DO→WRITE→CONTROL | לפי קבצים (workflows/nodes) | LangGraph, TypedDict, PydanticAI |
| **memory-feedback-node** | Memory Node כ־LangGraph node (feedback ל־Planner) | לפי קבצים (workflows/nodes) | LangGraph |
| **context-compression-and-optimization** | דחיסת context, חלון טוקנים | לפי קבצים (workflows/agents) | tiktoken, LangGraph |
| **api-interface-and-streaming** | API עם streaming (SSE/WebSocket), FastAPI | לפי קבצים (api, main.py) | FastAPI, Pydantic, Uvicorn, slowapi/fastapi-limiter, LangChain astream_events |
| **api-documentation-standards** | OpenAPI/Swagger, תיעוד API | לפי קבצים (api, routes) | FastAPI, Pydantic |
| **tests-and-validation** | מבנה טסטים, pytest, Arrange-Act-Assert | לפי קבצים (tests, test_*.py) | pytest |
| **llm-evaluation-and-metrics** | Evals ל־LLM, מטריקות איכות | לפי קבצים (evals, evaluation) | Ragas, DeepEval, pytest, Splunk |
| **data-migration-and-compatibility** | מיגרציות סכמה, תאימות לאחור | לפי קבצים (migrations, alembic) | Alembic, Flyway/Liquibase |
| **prompt-engineering-and-management** | ניהול פרומפטים, גרסאות, A/B | לפי קבצים (prompts) | Jinja2, LangChain PromptTemplates |
| **graph-traversal-testing** | בדיקות מסלול ב-workflow (רצף nodes) | לפי הקשר | LangGraph, Splunk/SPL |
| **simulation-and-property-testing** | בדיקות property, edge cases, chaos | לפי הקשר | Hypothesis, pytest |
| **bias-detection-and-ethics** | זיהוי הטיה, אתיקה, fairness | לפי הקשר | Splunk (דשבורדים) |
| **rules-management** | יצירה/עדכון של Rules (פורמט, מבנה) | לפי קבצים (RULE.mdc) | — |
| **helper-files-guide** | שימוש בקובצי עזר (examples) ל־Rules | לפי הקשר | — |
| **frontmatter-reference** | תבניות frontmatter לכל סוגי החוקים | לפי הקשר | — |
| **commands-management** | יצירה/עדכון של Commands | לפי קבצים (.cursor/commands/*.md) | — |

---

## פירוט לפי קטגוריות

### Core (`core/`)

#### core-python-standards
- **מה החוק אומר:** מתודולוגיית פיתוח: תכנון מערכת לפני קוד, אישור תוכנית, איכות קוד (שמות, type hints, guard clauses, DRY), פונקציות עד 20 שורות. Concurrency: asyncio ל־I/O, ProcessPoolExecutor ל־CPU. לוגים מובנים ל־Splunk, בלי `print`.
- **מתי נשתמש:** מופעל **תמיד** (Always Apply). רלוונטי בכל משימת קוד Python.
- **ספריות וטכנולוגיות:** `typing`, `asyncio`, `concurrent.futures.ProcessPoolExecutor`, `httpx`, Splunk (לוגים), `from __future__ import annotations`.
- **למחליט (האם לאמץ?):** מחייב תכנון לפני קוד, פונקציות קצרות וקריאות, וכתיבת לוגים מסודרת. מתאים לכל פרויקט Python שרוצים בו קוד אחיד וקל לתחזוקה. אם הצוות כבר עובד עם סטנדרטים דומים — החוק מקבע אותם; אם לא — הוא מעלה את הרף.

#### error-handling-and-resilience
- **מה החוק אומר:** סיווג שגיאות (transient vs permanent), retry עם exponential backoff ו־jitter, Tenacity, circuit breaker, DLQ, graceful degradation. אינטגרציה עם LangGraph (שדה errors, routing לשגיאות).
- **מתי נשתמש:** מופעל **תמיד** (Always Apply).
- **ספריות וטכנולוגיות:** Tenacity (`@retry`), circuitbreaker (או לוגיקה מותאמת), Splunk (אגרגציית שגיאות ב־SPL).
- **למחליט (האם לאמץ?):** מבטיח שהמערכת לא תיפול מכל שגיאה חולפת (רשת, rate limit) ותדע מתי לעצור ניסיונות. חובה אם יש קריאות ל־API חיצוניים או שירותים לא יציבים. מפחית תקלות בפרודקשן ומאפשר ניטור שגיאות מרוכז.

---

### Security (`security/`)

#### security-governance-and-observability
- **מה החוק אומר:** הגבלת blast radius, least privilege, רישום כלים מפורש, sandboxing. NIST AI RMF, OWASP Top 10 ל־LLM, Red Teaming, הערכה רציפה.
- **מתי נשתמש:** מופעל **תמיד** (Always Apply).
- **ספריות וטכנולוגיות:** אין ספריות ספציפיות; מפנה ל־api-interface-and-streaming (rate limits), monitoring-and-observability (audit/tracing).
- **למחליט (האם לאמץ?):** מגדיר איך לאבטח מערכות עם אג'נטים ו־LLM: כל אג'נט מקבל רק את מה שצריך, יש בקרה על פעולות קריטיות, ומתבצעת הערכה לפני פריסה. מתאים לפרויקטים עם רגישות אבטחתית או דרישות compliance.

#### audit-protocol
- **מה החוק אומר:** חובת audit trail: tool calls, state changes, API requests, גישה לנתונים, אירועי auth. מבנה לוג (timestamp, event_type, actor_id, correlation_id, וכו'), אחסון ב־Splunk (HEC), compliance (GDPR, HIPAA, SOC 2).
- **מתי נשתמש:** מופעל **תמיד** (Always Apply).
- **ספריות וטכנולוגיות:** Splunk, HEC (HTTP Event Collector).
- **למחליט (האם לאמץ?):** מבטיח שכל פעולה במערכת מתועדת וברת מעקב — מי עשה מה ומתי. חובה כשיש דרישות רגולטוריות או צורך לחקור תקלות ואחריות. דורש מערכת לוגים מרכזית (למשל Splunk).

#### prompt-injection-prevention
- **מה החוק אומר:** סניטציה ואימות של כל קלט משתמש לפני כניסה לפרומפטים; שכבות (escaping, filtering, validation); זיהוי דפוסי הזרקה; מניעת דליפת מידע ו־bypass של בקרות.
- **מתי נשתמש:** Apply Intelligently — כשעוסקים באבטחת קלט ו־LLM.
- **ספריות וטכנולוגיות:** אין ספריות חובה; דוגמאות ב־helper files.
- **למחליט (האם לאמץ?):** מגן מפני משתמשים שמנסים "לפרוץ" לפרומפטים (להכתיב לאג'נט הוראות או לחלץ מידע). חובה אם הקלט מגיע ממשתמשים חיצוניים או ממקורות לא מהימנים. מפחית סיכון להזרקת פרומפט ולחשיפת מידע רגיש.

---

### Agents (`agents/`)

#### planner-strategic-planning
- **מה החוק אומר:** חובת רכיב Planner: הגדרת מטרות, הערכת סיכונים, תוכנית פעולות לפני פירוק משימות. רץ לפני Orchestrator, מקבל feedback מ־Memory Node. מימוש כ־LangGraph node (READ→DO→WRITE→CONTROL).
- **מתי נשתמש:** Apply Intelligently —תכננים או משנים Planner.
- **ספריות וטכנולוגיות:** LangGraph.
- **למחליט (האם לאמץ?):** מחייב שלב "חשיבה" לפני ביצוע: האג'נט מגדיר מטרות ומעריך סיכונים לפני שהוא מפצל משימות. מתאים כשיש משימות מורכבות או סיכונים (עלות, בטיחות). עוזר למנוע פעולות מיותרות או מסוכנות.

#### executor-action-translation
- **מה החוק אומר:** רכיב Executor מתרגם תוכניות אסטרטגיות לאקשנים קונקרטיים (API, tools, DB, קבצים). מתאם ביצוע ומגיב לשינויים. מימוש כ־LangGraph node.
- **מתי נשתמש:** Apply Intelligently — כשמממשים או משנים Executor.
- **ספריות וטכנולוגיות:** LangChain (tool calls).
- **למחליט (האם לאמץ?):** מפריד בין "מה לעשות" (תוכנית) ל"איך לעשות" (קריאות לכלים ו־API). מתאים כשיש הרבה סוגי פעולות או צורך לשנות ביצוע בלי לגעת בתכנון. משפר סדר וארגון בקוד האג'נט.

#### memory-feedback-node
- **מה החוק אומר:** Memory Node כ־**node** ב־LangGraph (לא רק אחסון): מספק הקשר היסטורי ומשוב ל־Planner. אחסון חוויות, טעינת זיכרונות, לולאת feedback. משתמש ב־memory-and-archival-management לאחסון פיזי.
- **מתי נשתמש:** Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`.
- **ספריות וטכנולוגיות:** LangGraph.
- **למחליט (האם לאמץ?):** האג'נט לומד מההיסטוריה ומשפר החלטות — לא רק זוכר נתונים אלא מעביר תובנות חזרה ל־Planner. מתאים כשרוצים שהמערכת תשתפר לאורך זמן או תקח בחשבון ניסיונות קודמים.

#### memory-and-archival-management
- **מה החוק אומר:** זיכרון ארוך טווח במערכת נפרדת (Vector DB); זיכרון קצר ב־state של LangGraph. החלטה מתי Vector DB vs PostgreSQL; דפוס hybrid; חיפוש סמנטי, גרסאות, בידוד per user/tenant.
- **מתי נשתמש:** Apply Intelligently —תכננים זיכרון וארכיון.
- **ספריות וטכנולוגיות:** Vector DB, PostgreSQL, LangGraph state.
- **למחליט (האם לאמץ?):** מגדיר איך לשמור מידע בין שיחות ולחפש אותו (למשל "מה המשתמש אהב בעבר"). מתאים לאפליקציות אישיות או כשיש הרבה הקשר היסטורי. עוזר לבחור בין Vector DB ל־PostgreSQL לפי סוג השאילתות.

#### multi-agent-systems
- **מה החוק אומר:** ארכיטקטורה סטנדרטית: Orchestrator (פירוק ל־SECTIONS), Workers (מומחים), Synthesizer; מיקרו-אג'נטים במקום מונולית. Planner, Executor, Memory Node; FAN-OUT/FAN-IN, fallback.
- **מתי נשתמש:** Apply Intelligently — בבניית מערכות multi-agent.
- **ספריות וטכנולוגיות:** LangGraph, asyncio.gather.
- **למחליט (האם לאמץ?):** מגדיר איך לחלק עבודה בין אג'נטים: אחד מחלק משימות, אחרים מבצעים, ואחד מאחד תוצאות. מתאים כשיש משימות גדולות או צורך במומחיות שונה (למשל סיכום מול חיפוש). מונע "אג'נט ענק" אחד שעושה הכל.

#### agentic-logic-and-tools
- **מה החוק אומר:** LCEL, הגדרת כלים עם `@tool`, תיעוד כלים, binding ל־model. PydanticAI בתוך node ל־structured output; scratchpad ל־debug; cache ברמת מודול.
- **מתי נשתמש:** Apply Intelligently — בעבודה עם LangChain וכלים.
- **ספריות וטכנולוגיות:** LangChain, LCEL, PydanticAI.
- **למחליט (האם לאמץ?):** מקבע איך מגדירים כלים לאג'נט ואיך הוא משתמש בהם — תיעוד, פורמט פלט, וקאשינג. מתאים לכל פרויקט עם אג'נטים ו־LangChain. עוזר לאג'נט לבחור כלים נכון ולחסוך קריאות חוזרות.

#### contract-scope-and-boundaries
- **מה החוק אומר:** להגדיר חוזים מפורשים (Interface/ABC/Schema) **רק** בגבולות אינטגרציה (replaceability test). לא over-engineering בפנימיות. דוגמאות: Agent↔Tool, Planner↔Executor, LLM↔Code.
- **מתי נשתמש:** Apply Intelligently — בהחלטות ארכיטקטורה על חוזים.
- **ספריות וטכנולוגיות:** ABC, Pydantic, JSON Schema.
- **למחליט (האם לאמץ?):** עוזר להחליט איפה להשקיע בהגדרת ממשקים פורמליים ואיפה להשאיר קוד פשוט. מונע "יותר מדי" חוזים בפנימיות ומבטיח חוזים במקומות שבהם רוצים להחליף מימוש (ספק, צוות, טסטים).

#### agent-component-interfaces
- **מה החוק אומר:** חוזי API בין Planner, Memory Node, Executor באמצעות ABC ו־type hints. Pydantic למודלים מורכבים; החלפת מימושים ובדיקות עם mocks.
- **מתי נשתמש:** Apply Intelligently — בעיצוב ממשקי רכיבים.
- **ספריות וטכנולוגיות:** abc.ABC, Pydantic (מפנה ל־data-schemas-and-interfaces).
- **למחליט (האם לאמץ?):** מגדיר חוזה ברור בין רכיבי האג'נט (תכנון, זיכרון, ביצוע) — כל רכיב יודע מה הוא מקבל ומה הוא מחזיר. מתאים כשיש כמה מפתחים או רוצים להחליף מימוש (למשל Planner אחר) או לבדוק עם mocks.

#### langgraph-architecture-and-nodes
- **מה החוק אומר:** עיצוב workflow: state (TypedDict), edges, conditional routing. כל node: READ→DO→WRITE→CONTROL. PydanticAI אופציונלי בתוך node ל־DO (structured output). טיפול בשגיאות, checkpoints, interrupts. ויזואליזציה עם `get_graph().draw_png()`.
- **מתי נשתמש:** Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`.
- **ספריות וטכנולוגיות:** LangGraph, TypedDict, PydanticAI.
- **למחליט (האם לאמץ?):** מקבע מבנה אחיד ל־workflow: כל צומת קורא מידע, עושה עבודה, כותב ל־state, ומחליט לאן להמשיך. מתאים לכל פרויקט עם LangGraph. מקל על קריאה, דיבוג ותחזוקה — וגם על ויזואליזציה של הזרימה.

#### cost-and-budget-management
- **מה החוק אומר:** שדה BudgetState ב־GraphState; מעקב טוקנים ועלות בזמן אמת; סף אזהרה וסף קשיח; עצירת agent כשחורג מתקציב.
- **מתי נשתמש:** Apply Intelligently — במערכות עם לולאות ו־LLM calls.
- **ספריות וטכנולוגיות:** LangGraph (state).
- **למחליט (האם לאמץ?):** מונע עלויות טוקנים שיוצאות משליטה — האג'נט עוצר כשמגיע לתקציב מוגדר. חובה כשיש קריאות LLM בתשלום או לולאות שיכולות לרוץ ללא הגבלה. חוסך הפתעות בחשבון ומאפשר שליטה בעלויות.

#### human-in-the-loop-approval
- **מה החוק אומר:** סכמת Approval Context ל־interrupts: risk_level, estimated_cost, proposed_diff, action_description, current_state_snapshot, וכו'. אינטגרציה עם LangGraph interrupts.
- **מתי נשתמש:** Apply Intelligently — כשמממשים HITL.
- **ספריות וטכנולוגיות:** LangGraph (interrupts).
- **למחליט (האם לאמץ?):** כשהאג'נט עוצר ומבקש אישור אדם — האדם מקבל הקשר מובנה: רמת סיכון, עלות משוערת, מה בדיוק יישמר. מתאים לפעולות רגישות (מחיקה, פריסה, תשלום). עוזר לאשר או לדחות בצורה מושכלת.

#### model-routing-and-selection
- **מה החוק אומר:** ניתוב דינמי לפי מורכבות משימה: מודלים קטנים/זולים למשימות פשוטות, חזקים למורכבות. הערכת complexity, capability matrix, טיירים (Haiku/Flash vs Sonnet vs Opus).
- **מתי נשתמש:** Apply Intelligently — באופטימיזציית עלות/ביצועים.
- **ספריות וטכנולוגיות:** Splunk (מטריקות, ניטור).
- **למחליט (האם לאמץ?):** לא כל משימה צריכה את המודל הכי יקר — סיווג פשוט יכול ללכת למודל זול, לוגיקה מורכבת למודל חזק. מפחית עלויות טוקנים בלי לפגוע באיכות. מתאים כשיש שימוש בכמה מודלים או תקציב מוגבל.

#### context-compression-and-optimization
- **מה החוק אומר:** ניטור גודל חלון ה־context; סף אזהרה/דחיסה; אסטרטגיות summarization (extractive/abstractive); ניקוי הודעות ישנות; יישור ל־LangGraph state.
- **מתי נשתמש:** Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/agents/**/*.py`.
- **ספריות וטכנולוגיות:** tiktoken (או מונה טוקנים), LangGraph.
- **למחליט (האם לאמץ?):** כשהשיחה או ה־workflow ארוכים, חלון ה־context מתמלא — החוק מגדיר מתי לדחוס, לסכם או לנקות. חוסך טוקנים ומונע חיתוך מידע חשוב. מתאים לשיחות ארוכות או workflows עם הרבה state.

#### reflection-and-self-critique
- **מה החוק אומר:** חובת Reviewer Node לפני Synthesizer: הערכת איכות, critique, לולאת revision עד סף איכות או מקסימום איטרציות.
- **מתי נשתמש:** Apply Intelligently — בשיפור איכות פלט.
- **ספריות וטכנולוגיות:** אין ספריות חובה.
- **למחליט (האם לאמץ?):** האג'נט בודק את עצמו לפני שמגיש תוצאה — "דור שני" מעריך ומבקש תיקונים. מעלה איכות פלט ומפחית טעויות גסות. מתאים כשאיכות התוצאה קריטית (דוחות, המלצות, תשובות ללקוח).

---

### Infrastructure (`infrastructure/`)

#### uvicorn-asgi-server
- **מה החוק אומר:** Uvicorn כשרת ASGI היחיד; התקנה עם `uvicorn[standard]` (uvloop, httptools, watchfiles). פיתוח: `--reload`; פרודקשן: `--workers` בלי `--reload`.
- **מתי נשתמש:** Apply Intelligently — בהרצת אפליקציות FastAPI/ASGI.
- **ספריות וטכנולוגיות:** Uvicorn, uvloop, httptools, watchfiles.
- **למחליט (האם לאמץ?):** מקבע שרת אחד להרצת FastAPI — אותו כלי בפיתוח ובפרודקשן, עם הגדרות ברורות (reload בפיתוח, workers בפרודקשן). מונע בלבול ובעיות תאימות. מתאים לכל פרויקט שמריץ API ב־Python.

#### deployment-and-infrastructure
- **מה החוק אומר:** CI/CD (lint, test, build, security scan, deploy); Docker כ־default: multi-stage, base image מקובע, non-root, בלי secrets בתמונה, סריקת image (Trivy/Snyk); לוגים ל־stdout/stderr; Docker Compose ל־dev; Kubernetes ל־staging/prod.
- **מתי נשתמש:** Apply Intelligently — בפריסה ותשתית.
- **ספריות וטכנולוגיות:** Docker, Kubernetes, Uvicorn, Splunk (לוגים), ruff/black/mypy.
- **למחליט (האם לאמץ?):** מגדיר איך בונים, סורקים ומפריסים את האפליקציה — צינור אוטומטי, קונטיינרים מאובטחים, ולוגים שניתן לאסוף. מתאים לפרויקטים שמועלים לפרודקשן או ל־staging. מפחית טעויות ידניות וחשיפת סודות.

#### monitoring-and-observability
- **מה החוק אומר:** Splunk כפלטפורמה אחת למטריקות, לוגים ו־tracing. HEC להזנה; SPL לשאילתות. שדות חובה: timestamp, correlation_id, duration_ms; PerformanceTimer; span events.
- **מתי נשתמש:** Apply Intelligently — בניטור ו־observability.
- **ספריות וטכנולוגיות:** Splunk, HEC, SPL.
- **למחליט (האם לאמץ?):** מקבע מקום אחד לכל הלוגים והמטריקות — אפשר לעקוב אחרי בקשה מקצה לקצה, למדוד זמנים ולחפש תקלות. חובה כשיש צורך לאבחן בעיות בפרודקשן או לעמוד ב־SLA. דורש Splunk (או תשתית דומה).

#### rate-limiting-and-queue-management
- **מה החוק אומר:** rate limiting ברמת agent וגלובלית; תורים (FIFO/priority) כשמגיעים למגבלות; exponential backoff. בשכבת HTTP — FastAPI middleware (מפנה ל־api-interface-and-streaming).
- **מתי נשתמש:** Apply Intelligently — במערכות multi-agent ו־API.
- **ספריות וטכנולוגיות:** FastAPI (middleware/dependencies).
- **למחליט (האם לאמץ?):** מונע "הצפה" של קריאות ל־API חיצוני (למשל OpenAI) — חלוקה הוגנת בין אג'נטים ותור כשמגיעים למגבלה. חובה כשיש הרבה אג'נטים במקביל או מגבלות ספק. מפחית 429 ותקלות רשת.

#### performance-optimization
- **מה החוק אומר:** קאשינג (Redis, in-memory, CDN); cache-aside/write-through/write-back; אופטימיזציית שאילתות; connection pooling; msgpack/orjson.
- **מתי נשתמש:** Apply Intelligently — באופטימיזציית ביצועים.
- **ספריות וטכנולוגיות:** Redis, functools.lru_cache, CDN.
- **למחליט (האם לאמץ?):** מגדיר מתי לשמור תוצאות (cache), איך לנצל חיבורים מחדש (pooling), ואיך להאיץ שאילתות. מתאים כשיש צוואר בקבוק ב־DB או ב־API. מפחית עומס ולטנציה בלי לשנות לוגיקה עסקית.

#### multi-tenancy-and-isolation
- **מה החוק אומר:** אסטרטגיות בידוד: DB נפרד / schema / row-level (tenant_id); חובת validation בשכבת האפליקציה; דפוסי query בטוחים.
- **מתי נשתמש:** Apply Intelligently — במערכות multi-tenant.
- **ספריות וטכנולוגיות:** PostgreSQL (schemas, tenant_id).
- **למחליט (האם לאמץ?):** מגדיר איך להפריד נתונים בין לקוחות (tenants) — שלא יראו או ישנו נתונים אחד של השני. חובה ב־SaaS או כשמשרתים כמה ארגונים. עוזר לבחור רמת בידוד (DB / schema / שורה) לפי צורך ואכיפת tenant_id בכל שאילתה.

---

### Development (`development/`)

#### tests-and-validation
- **מה החוק אומר:** pytest כפריימוורק; תיקיית `tests/`, קבצים `test_<component>.py`; טסטים אטומיים; Arrange-Act-Assert; mocking ל־API חיצוני; סימנים ויזואליים (✅/❌/⚠️).
- **מתי נשתמש:** Apply to Specific Files — `**/tests/**/*.py`, `**/test_*.py`.
- **ספריות וטכנולוגיות:** pytest.
- **למחליט (האם לאמץ?):** מקבע איך כותבים ומריצים טסטים — מבנה תיקיות, פורמט פלט ברור, וטסט אחד לרעיון אחד. מתאים לכל פרויקט שרוצים בו regression מונע ו־CI יציב. מקל על מפתחים חדשים להבין איפה לכתוב טסט.

#### code-review-and-collaboration
- **מה החוק אומר:** צ'קליסט ל־PR (איכות, פונקציונליות, טסטים, תיעוד, אבטחה); Git workflow עם GitFlow; branch protection.
- **מתי נשתמש:** Apply Intelligently — ב־code review ושיתוף פעולה.
- **ספריות וטכנולוגיות:** ruff, black; מפנה ל־gitflow-branching-model.
- **למחליט (האם לאמץ?):** נותן רשימת בדיקות ברורה ל־PR ומגדיר איך עובדים עם ענפים (feature, release, hotfix). מתאים לצוותים שרוצים אחידות ב־review ומניעת merge ישיר ל־master. משפר איכות קוד ושיתוף פעולה.

#### versioning-and-release-management
- **מה החוק אומר:** גרסאות סמנטיות (MAJOR.MINOR.PATCH); CHANGELOG (Keep a Changelog); pre-release (alpha, beta, rc); feature flags.
- **מתי נשתמש:** Apply Intelligently — בניהול גרסאות ושחרורים.
- **ספריות וטכנולוגיות:** Keep a Changelog (פורמט).
- **למחליט (האם לאמץ?):** מקבע איך מסמנים גרסאות ומתעדים שינויים — מספר גרסה שמשקף breaking vs feature vs fix, ו־CHANGELOG שמסביר מה השתנה. מתאים למוצר שמשחררים ללקוחות או לצורך rollback ברור. מקל על תאימות ותקשורת.

#### gitflow-branching-model
- **מה החוק אומר:** GitFlow בלבד: master (production), develop (אינטגרציה); feature מ־develop; release מ־develop → merge ל־master ו־develop; hotfix מ־master → merge ל־master ו־develop. אין push ישיר ל־master/develop.
- **מתי נשתמש:** Apply Intelligently — בעבודה עם ענפים.
- **ספריות וטכנולוגיות:** Git.
- **למחליט (האם לאמץ?):** מגדיר איזה ענף לכל סוג עבודה ואיפה למזג — פיצ'רים נכנסים ל־develop, שחרורים דרך release, תיקונים דחופים דרך hotfix. מתאים לפרויקטים עם גרסאות פרודקשן ורצון ליציבות. מונע בלבול ו־merge ישיר ל־production.

---

### API (`api/`)

#### api-interface-and-streaming
- **מה החוק אומר:** FastAPI כפריימוורק; streaming (SSE/WebSocket) חובה לאג'נטים; Pydantic ל־request/response; OpenAPI ב־/openapi.json ו־/docs; Uvicorn (ראה uvicorn-asgi-server); rate limiting (slowapi/fastapi-limiter); אירועים מובנים (token, tool_start, tool_end, error); LangChain astream_events.
- **מתי נשתמש:** Apply to Specific Files — `**/api/**/*.py`, `**/routes/**/*.py`, `**/main.py`.
- **ספריות וטכנולוגיות:** FastAPI, Pydantic, Uvicorn, slowapi או fastapi-limiter, LangChain (astream_events).
- **למחליט (האם לאמץ?):** מקבע stack ל־API: FastAPI, streaming כדי שהלקוח יקבל עדכונים בזמן אמת (חשוב לאג'נטים), תיעוד אוטומטי ו־rate limiting. מתאים לכל שירות API ב־Python, במיוחד כשיש אג'נטים או תגובות ארוכות.

#### api-documentation-standards
- **מה החוק אומר:** תיעוד OpenAPI 3.0; שימוש ב־FastAPI ל־schema אוטומטי; תיאור request/response; גרסאות API (URL או header); deprecation ו־migration.
- **מתי נשתמש:** Apply to Specific Files — `**/api/**/*.py`, `**/routes/**/*.py`, `**/endpoints/**/*.py`.
- **ספריות וטכנולוגיות:** FastAPI, Pydantic.
- **למחליט (האם לאמץ?):** מבטיח שה־API מתועד וברור — סכמות, דוגמאות, גרסאות ו־deprecation מסודרת. מתאים כשיש צרכנים חיצוניים או צוותים שמשתמשים ב־API. מפחית טעויות אינטגרציה ומקל על שינויים breaking.

#### mcp-protocol-implementation
- **מה החוק אומר:** כלים לאג'נטים דרך Model Context Protocol (MCP); שרת MCP אחד עם Views/Profiles/Scopes; גילוי כלים דינמי; JSON-RPC, Tools/Resources/Prompts.
- **מתי נשתמש:** Apply Intelligently — במימוש MCP servers/clients.
- **ספריות וטכנולוגיות:** MCP (mcp.server, stdio_server), JSON-RPC 2.0.
- **למחליט (האם לאמץ?):** מגדיר איך לחבר אג'נטים לכלים חיצוניים בתקן אחד — כלים מתגלים בזמן ריצה, אפשר להחליף או להוסיף בלי לשנות קוד האג'נט. מתאים כשיש הרבה כלים או צורך ב־Views/Profiles שונים (למשל סביבות dev vs prod).

---

### Data (`data/`)

#### data-schemas-and-interfaces
- **מה החוק אומר:** בגבולות (Agent↔Tool, API) — Pydantic BaseModel; בפנימי — dataclass. Field(description=) חובה; Literal לערכים מוגבלים; serialization עם .json()/.parse_raw(); structured outputs ו־bind_tools.
- **מתי נשתמש:** Apply Intelligently — בהגדרת סכמות ומודלים. מפנה ל־contract-scope-and-boundaries.
- **ספריות וטכנולוגיות:** Pydantic (BaseModel, Field), typing.Literal.
- **למחליט (האם לאמץ?):** מקבע איך מגדירים מבני נתונים בגבולות (API, כלים, פלט LLM) — אימות אוטומטי, תיאורים ל־LLM, ופורמט אחיד. מתאים לכל פרויקט עם API או אג'נטים. מפחית באגים של קלט/פלט לא חוקי.

#### data-migration-and-compatibility
- **מה החוק אומר:** מיגרציות עם Alembic (או Flyway/Liquibase); idempotent, reversible, atomic; תאימות לאחור (API, schema, client); ETL ודפוסי טרנספורמציה.
- **מתי נשתמש:** Apply to Specific Files — `**/migrations/**/*.py`, `**/alembic/**/*.py`.
- **ספריות וטכנולוגיות:** Alembic, SQLAlchemy; Flyway/Liquibase (לא־Python).
- **למחליט (האם לאמץ?):** מגדיר איך משנים סכמת DB בבטחה — מיגרציות שניתן להריץ ולהחזיר אחורה, בלי לשבור גרסאות קיימות. חובה כשיש שינויי טבלאות/שדות או דרישת תאימות ללקוחות ישנים. מפחית סיכון בפריסות.

---

### Evaluation (`evaluation/`)

#### llm-evaluation-and-metrics
- **מה החוק אומר:** Evals ל־LLM (מעבר ל־pytest): Faithfulness, Answer Relevance, Context Precision, Tool Usage Accuracy. Ragas או DeepEval; תוצאות ל־Splunk (HEC, SPL). Golden datasets, CI על subset.
- **מתי נשתמש:** Apply to Specific Files — `**/evals/**/*.py`, `**/evaluation/**/*.py`.
- **ספריות וטכנולוגיות:** Ragas, DeepEval, pytest, Splunk.
- **למחליט (האם לאמץ?):** מודד איכות תשובות האג'נט — נאמנות למקור, רלוונטיות, שימוש נכון בכלים — לא רק "הקוד רץ". מתאים כשאיכות התוכן קריטית או יש דרישות איכות. עוזר לתפוס הולוצינציות ורגרסיות לפני פרודקשן.

#### llm-judge-protocol
- **מה החוק אומר:** פרוטוקול LLM-as-Judge: הערכת correctness, tool usage, יעילות, אבטחה ופרטיות על בסיס execution logs, audit tables, מטריקות ו־final output.
- **מתי נשתמש:** Apply Intelligently — בהערכת מערכות אג'נטיות.
- **ספריות וטכנולוגיות:** אין ספריות חובה.
- **למחליט (האם לאמץ?):** מגדיר איך "שופט" (LLM או אדם) מעריך ריצות אג'נט — נכונות, שימוש בכלים, יעילות ואבטחה. מתאים ל־QA מתקדם, ביקורות לפני שחרור, או ניתוח אחרי תקלה. משלים טסטים אוטומטיים בהערכת איכות ורציונל.

#### graph-traversal-testing
- **מה החוק אומר:** בדיקות שמאמתות רצף nodes ב־workflow (expected path, forbidden path, coverage); שימוש ב־traces (למשל מ־Splunk/SPL) לאימות.
- **מתי נשתמש:** Apply Intelligently — בבדיקות workflow.
- **ספריות וטכנולוגיות:** LangGraph, Splunk/SPL.
- **למחליט (האם לאמץ?):** בודק שלא רק התוצאה נכונה אלא שהאג'נט עבר במסלול הנכון ב־workflow (הצמתים והסדר). מתאים כשיש הרבה ענפים או סיכון ששינוי קטן ישבור את הזרימה. תופס באגים שטסטים על פלט סופי לא יתפסו.

#### simulation-and-property-testing
- **מה החוק אומר:** בדיקות property-based עם Hypothesis; edge cases, chaos; invariants (פורמט פלט, state consistency); אינטגרציה עם pytest.
- **מתי נשתמש:** Apply Intelligently — בבדיקות resilience ו־edge cases.
- **ספריות וטכנולוגיות:** Hypothesis, pytest.
- **למחליט (האם לאמץ?):** מייצר אוטומטית הרבה מקרי קיצון (ריק, ארוך, שגיאות) ובודק שהמערכת לא נשברת. מתאים למערכות שצריכות לעמוד בתנאים קשים או כשיש חשש לבאגים נדירים. משלים טסטים ידניים בגילוי בעיות לא צפויות.

#### bias-detection-and-ethics
- **מה החוק אומר:** זיהוי והפחתת הטיה (דמוגרפית, תרבותית, זיכרון ארוך טווח); מטריקות fairness; דשבורדים ב־Splunk.
- **מתי נשתמש:** Apply Intelligently — באתיקה והגינות.
- **ספריות וטכנולוגיות:** Splunk (מטריקות, דשבורדים).
- **למחליט (האם לאמץ?):** מגדיר איך למדוד ולהקטין הטיה בתשובות האג'נט (למשל לפי קבוצות אוכלוסייה או לאורך זמן). מתאים למוצרים עם השפעה על אנשים או דרישות הגינות. עוזר לעמוד בדרישות אתיות ורגולטוריות.

#### final-review-protocol
- **מה החוק אומר:** צ'קליסט חובה לפני שליחת תשובה: פונקציות עד 20 שורות, asyncio/ProcessPoolExecutor, typing, logger, nodes READ→DO→WRITE→CONTROL, Tenacity, pydantic-settings, pytest, Docker, API docs, וכו'.
- **מתי נשתמש:** מופעל **תמיד** (Always Apply).
- **ספריות וטכנולוגיות:** pydantic-settings, pytest, Docker, FastAPI (תיעוד), Tenacity.
- **למחליט (האם לאמץ?):** מאלץ סיבוב בדיקה אחרון לפני שהאג'נט "מגיש" — שהקוד עומד בסטנדרטים (אורך פונקציות, טיפול בשגיאות, תיעוד, טסטים). מתאים כשהרובוט (Cursor) מייצר קוד ורוצים שלא יישכחו פריטים בסיסיים. משמש כ־safety net.

---

### Configuration (`configuration/`)

#### configuration-and-dependency-injection
- **מה החוק אומר:** pydantic-settings לכל הקונפיגורציה; validation ב־startup; SecretStr לרגישים; אין הדפסת config ללוגים בלי masking.
- **מתי נשתמש:** Apply Intelligently — בניהול קונפיגורציה.
- **ספריות וטכנולוגיות:** pydantic-settings, SecretStr.
- **למחליט (האם לאמץ?):** מקבע איך טוענים הגדרות (env, קבצים) — אימות בהפעלה, סודות לא נחשפים בלוגים. מתאים לכל אפליקציה עם config או secrets. מפחית באגי קונפיגורציה ודליפות.

#### prompt-engineering-and-management
- **מה החוק אומר:** פרומפטים לא כמחרוזות בקוד; קבצים/תיקייה ייעודית; Jinja2 או LangChain PromptTemplates; תגיות XML; גרסאות ו־A/B testing לפרומפטים.
- **מתי נשתמש:** Apply to Specific Files — `**/prompts/**/*.py`, `**/prompts/**/*.yaml`, `**/prompts/**/*.txt`.
- **ספריות וטכנולוגיות:** Jinja2, LangChain PromptTemplates.
- **למחליט (האם לאמץ?):** מפריד פרומפטים מהלוגיקה — קל לערוך, לגרס ו־להשוות גרסאות (A/B). מתאים כשיש הרבה פרומפטים או צורך לשפר אותם בלי לגעת בקוד. משפר שליטה ואיכות בתשובות האג'נט.

---

### ניהול חוקים ו־Commands (Meta)

#### rules-management
- **מה החוק אומר:** פורמט ו־מבנה ליצירה/עדכון Rules: תיקייה עם RULE.mdc, frontmatter לפי סוג (Always / Intelligently / Specific Files / Manual), תוכן מובנה. מפנה ל־helper-files-guide ו־frontmatter-reference.
- **מתי נשתמש:** Apply to Specific Files — `**/.cursor/rules/**/RULE.mdc`.
- **ספריות וטכנולוגיות:** אין.
- **למחליט (האם לאמץ?):** מגדיר איך כותבים ועורכים חוקי Cursor — מבנה קובץ, סוג הפעלה, ואיפה לשים דוגמאות. רלוונטי למי שמוסיף או משנה Rules בפרויקט. שומר על אחידות וקריאות של כל החוקים.

#### helper-files-guide
- **מה החוק אומר:** שימוש בקובצי עזר (examples_*.py) במקום קוד ארוך ב־RULE.mdc; שמירה על Rules מתחת ל־400 שורות; ארגון בתיקיית החוק.
- **מתי נשתמש:** Apply Intelligently — בעת כתיבת/עדכון Rules עם דוגמאות.
- **ספריות וטכנולוגיות:** אין.
- **למחליט (האם לאמץ?):** עוזר לשמור על חוקים קצרים וברורים — דוגמאות קוד בקובץ נפרד במקום בתוך החוק. מתאים למי שמוסיף Rules עם הרבה דוגמאות. מקל על תחזוקה ועדכון.

#### frontmatter-reference
- **מה החוק אומר:** תבניות frontmatter מלאות לכל ארבעת סוגי החוקים (Always Apply, Apply Intelligently, Apply to Specific Files, Apply Manually).
- **מתי נשתמש:** Apply Intelligently — בעת יצירת/עדכון Rules.
- **ספריות וטכנולוגיות:** אין.
- **למחליט (האם לאמץ?):** מספק העתק-הדבק ל־YAML בראש כל חוק — מתי הוא רץ (תמיד / לפי הקשר / לפי קבצים). רלוונטי למי שיוצר או מעדכן Rules. מונע טעויות ב־frontmatter ומבטיח שהחוק יופעל כמו שמתכוונים.

#### commands-management
- **מה החוק אומר:** פורמט ומבנה ל־Cursor Commands: קבצי .md ב־.cursor/commands, כותרת H1, תיאור, שלבים, Rules Applied.
- **מתי נשתמש:** Apply to Specific Files — `**/.cursor/commands/**/*.md`.
- **ספריות וטכנולוגיות:** אין.
- **למחליט (האם לאמץ?):** מגדיר איך כותבים פקודות Cursor (למשל `/test` או `/deploy`) — מבנה, שלבים, ואילו Rules מחוברים. רלוונטי למי שיוצר או משנה Commands. שומר על פקודות אחידות וניתנות לשימוש חוזר.

---

## קישורים

- **[README.md](README.md)** — תיעוד מלא באנגלית (מבנה, סוגי חוקים, דוגמאות הפעלה).
- **[Commands](../commands/README.md)** — תיעוד Commands.
- **[Rules Management](rules-management/RULE.mdc)** — מפרט יצירה/עדכון Rules.
