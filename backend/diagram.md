```mermaid
graph TD
    Client[Client Web] -->|HTTP Requests| API[FastAPI API]
    
    subgraph Backend
        API -->|Routes| Auth[Auth Routes]
        API -->|Routes| Questions[Questions Routes]
        API -->|Routes| Responses[Responses Routes]
        API -->|Routes| Admin[Admin Routes]
        
        Auth -->|Dépendances| DB[(PostgreSQL)]
        Questions -->|Dépendances| DB
        Responses -->|Dépendances| DB
        Admin -->|Dépendances| DB
        
        Auth -->|Utilise| Security[Security Utils]
        Auth -->|Utilise| Email[Email Utils]
        
        subgraph Models
            UserModel[User Model]
            QuestionModel[Question Model]
            ResponseModel[Response Model]
        end
        
        subgraph Schemas
            UserSchema[User Schema]
            QuestionSchema[Question Schema]
            ResponseSchema[Response Schema]
            TokenSchema[Token Schema]
        end
        
        DB -->|ORM| Models
        Auth -->|Validation| UserSchema
        Auth -->|Validation| TokenSchema
        Questions -->|Validation| QuestionSchema
        Responses -->|Validation| ResponseSchema
    end
