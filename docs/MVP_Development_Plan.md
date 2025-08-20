# Access Rating Scheme - Solo Dev MVP Roadmap

This roadmap reflects the actual state of the codebase as of August 2025.

## Core Stack

- Django REST API (backend)
- PostgreSQL (DB)
- Docker for dev/prod

## Key Practices

- Pre-commit: black, isort, flake8, detect-secrets
- Use features_to_implement.md as your actionable backlog

## Roadmap & Status

**Phase 1: Backend MVP (done)**
- Django project setup
- Business model (core fields, admin interface)
- User authentication (accounts app, profile, favorites)
- REST API endpoints for business, photo, review, favorites
- Business photo and review models/endpoints

**Phase 2: User Features (partially done)**
- JWT auth, user profile, favorites (implemented)
- Business reviews and photos (implemented)
- User registration/login (backend present, frontend needed)
- Business claiming (not yet implemented)
- QR code generation (not yet implemented)
- User dashboard (not yet implemented)

**Phase 3: Assessment Workflow (planned/simplified)**
- Google Forms for volunteer assessments (external/manual)
- Admin manual entry of ratings (via Django admin)
- QR/sticker tracking (not yet implemented)

**Phase 4: Polish & Scale (planned)**
- Google Maps, filtering, image optimization, review moderation, analytics, Docker, CI/CD (not yet implemented)

**Phase 5: Production Launch (planned)**
- Deploy, SSL, backup, UAT, legal pages, feedback (not yet implemented)

**Future**
- PostGIS, mobile app, advanced analytics, integrations

## Dev Workflow

1. Setup venv & install deps
2. Run pre-commit install
3. Use black, isort, flake8, detect-secrets (pre-commit)
4. Use Docker for deployment
5. Use features_to_implement.md for backlog

## Status

Backend MVP: business model, user auth, favorites, reviews, and photos are implemented. No QR code, business claiming, or advanced features yet. See features_to_implement.md for next steps.

---
_Solo dev streamlined plan. Remove/expand as needed._
## 🚀 Development Approach

### MVP Philosophy

- **Lightweight**: Start simple, iterate based on feedback
- **Scalable**: Architecture supports growth to production system
- **Professional**: Industry-standard practices and clean code
- **API-First**: Complete frontend/backend separation

### Key Design Decisions

- **Stateless Authentication**: JWT for mobile/web compatibility
- **Immutable Assessments**: Audit trail for official ratings
- **Modular Architecture**: Separate apps for clear concerns
- **Simple Location Storage**: Latitude/longitude coordinates for basic mapping

## 📊 Data Model Overview

```
User (Django Auth)
├── Business (Central entity)
│   ├── Assessment (Official ratings 1-5)
│   ├── Reviews (Public feedback)
│   ├── Photos (Visual documentation)
│   └── Sticker (QR codes and requests)
└── Favorites (Saved businesses)
```

## 🎯 Business Model

- **Revenue**: £30 assessment fee per business
- **Value Prop**: Increased disabled customer confidence and business inclusivity awareness
- **Growth**: Voluntary participation with clear ROI for businesses

## 🔮 Future Enhancements

- **Advanced Geographic Features**: PostGIS for complex radius queries and spatial indexing
- **Advanced Moderation**: AI-assisted review filtering
- **Mobile App**: Native iOS/Android applications
- **Integration**: Enhanced Google Maps features, accessibility databases
- **Analytics**: Business dashboard with visitor insights

## 🏃‍♂️ Getting Started

1. **Setup Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

4. **Frontend Development**

   ```bash
   cd frontend
   npm install
   npm start
   ```

## 📋 Project Status

**Current Phase**: Backend MVP Complete (Phase 1)  
**Next Steps**: Frontend React development (Phase 2)  
**Goal**: Working MVP for proof-of-concept and potential funding

## 🗓️ Development Phases

### **Phase 1: MVP Core (4-6 weeks)** ✅ COMPLETE

**Goal**: Basic working system for proof-of-concept

**Backend Implementation:**

- ✅ Django project setup with PostgreSQL
- ✅ Basic user authentication (Django admin only)
- ✅ Business model with core fields:
  - Name, address, business type
  - Simple description
  - Accessibility rating (1-5)
  - Basic contact info
- ✅ Admin interface for adding/editing businesses
- ✅ REST API endpoints for business listings
- ✅ QR code generation utility

**Frontend Implementation:**

- 🚧 React app setup with routing
- 🚧 Business listing page
- 🚧 Business detail page with QR code
- 🚧 Basic responsive design
- 🚧 API integration with Django backend

**Success Criteria:**

- Admin can add businesses via Django admin
- Public can view business list and details
- QR codes generate and link to business pages
- System works on desktop and mobile browsers

### **Phase 2: User Features (3-4 weeks)** 🚧 IN PROGRESS

**Goal**: Add public user engagement and basic business owner features

**New Features:**

- ✅ JWT authentication system (backend complete)
- 🚧 Public user registration and login (frontend needed)
- 🚧 Business owner account type (frontend needed)
- 🚧 Business claiming process (frontend needed)
- ✅ Basic review system (backend complete)
- ✅ Photo upload for businesses (backend complete)
- 🚧 User favorites system (frontend needed)

**Enhanced Features:**

- 🚧 Improved business detail pages (frontend needed)
- 🚧 User dashboard (frontend needed)
- ✅ Basic search functionality (backend complete)

### **Phase 3: Assessment Workflow (SIMPLIFIED)** ✅ SIMPLIFIED

**Goal**: Streamlined assessment process without complex app architecture

**Simplified Process:**

- ✅ Google Forms for volunteer assessments (external)
- ✅ Admin manually enters ratings via Django admin
- ✅ Business model stores all rating data
- ✅ QR code generation built into Business model
- ✅ Sticker requests tracked via business fields

**Eliminated Complexity:**

- ❌ No separate assessments app
- ❌ No complex workflow system
- ❌ No separate stickers app
- ❌ No assessment approval pipeline

**Benefits:**

- Faster MVP development
- Simpler maintenance
- Google Forms provides better UX for volunteers
- Manual process allows for quality control

**Enhanced Features:**

- ⏳ Improved admin dashboard
- ⏳ Assessment scheduling system
- ⏳ Business owner assessment requests

### **Phase 4: Polish & Scale (2-3 weeks)** ⏳ PLANNED

**Goal**: Production-ready system with enhanced features

**New Features:**

- 🚧 Basic location display with Google Maps
- 🚧 Advanced filtering and sorting
- 🚧 Image optimization and multiple photos
- 🚧 Sticker request and tracking system
- 🚧 Review moderation system
- 🚧 Basic analytics dashboard

**Technical Improvements:**

- 🚧 Redis caching for performance
- 🚧 Docker containerization
- 🚧 CI/CD pipeline setup
- 🚧 Error monitoring and logging
- 🚧 API documentation

### **Phase 5: Production Launch (2-3 weeks)** ⏳ PLANNED

**Goal**: Live system ready for real users

**Launch Preparation:**

- ⏳ Production deployment setup
- ⏳ Domain and SSL configuration
- ⏳ Database backup and recovery
- ⏳ User acceptance testing
- ⏳ Content management system
- ⏳ Legal pages (privacy policy, terms)

**Post-Launch:**

- ⏳ User feedback collection
- ⏳ Performance monitoring
- ⏳ Bug fixes and improvements
- ⏳ Feature prioritization based on usage

### **Future Phases (Post-Launch)**

**Phase 6: Advanced Features**

- PostGIS implementation for advanced geographic queries
- Mobile app development
- Advanced analytics and reporting
- Integration with external accessibility databases
- Multi-language support
- Complex radius-based business searches

**Phase 7: Business Growth**

- Business dashboard with insights
- Automated assessment reminders
- Bulk sticker ordering system
- API for third-party integrations
- White-label solutions for local councils

---

**Total MVP Timeline**: 12-16 weeks to production-ready system  
**Minimum Viable Timeline**: 4-6 weeks for proof-of-concept

_This project aims to make physical spaces more accessible for everyone while supporting businesses in their inclusivity journey._
