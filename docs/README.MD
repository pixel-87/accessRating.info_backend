# Access Rating Scheme - MVP Platform

A UK-focused accessibility rating platform for physical businesses, providing clear visual ratings similar to the UK's food hygiene sticker system.

## 🎯 Project Overview

**Mission**: Empower disabled individuals with reliable accessibility information while raising business awareness about inclusivity.

**Core Concept**: Voluntary rating scheme (1-5 scale) for businesses, with physical QR code stickers linking to detailed online profiles.

## 🏗️ System Architecture

```
React Frontend ↔ Django REST API ↔ PostgreSQL Database
```

### Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: React (decoupled SPA)
- **Database**: PostgreSQL (with PostGIS for geographic queries)
- **Authentication**: JWT tokens via djangorestframework-simplejwt
- **DevOps**: Docker, environment variables
- **Caching**: Redis (future enhancement)

### App Structure

```
apps/
├── accounts/     # User management, JWT auth, roles
├── businesses/   # Business profiles, contact info, photos
├── assessments/  # Official ratings, reports, volunteer workflow
├── reviews/      # Public feedback system (eBay-style)
└── stickers/     # QR generation, physical sticker requests
```

## 👥 User Roles

### Public Users

- View business accessibility ratings
- Leave feedback (positive/neutral/negative + comments)
- Save favorites and share businesses
- Scan QR codes for instant access

### Business Owners

- Claim and edit business listings
- Upload photos and accessibility notes
- Update opening hours and contact info
- Request assessments and replacement stickers

### Admins/Volunteers

- Conduct accessibility assessments (1-5 rating)
- Approve official ratings and reports
- Manage user accounts and moderate reviews
- Handle sticker printing and fulfillment

## 🏪 Rating System

**1**: Limited mobility friendly (elderly, walking aids, visually impaired)  
**2**: Wheelchair accessible entry (step-free, wide doorways)  
**3**: Accessible bathroom with grab bars and turning space  
**4**: Changing Places bathroom with hoist and shower  
**5**: Fully accessible with event hosting capabilities  

## 🔧 Core Features (MVP)

### Business Profiles

- Name, address, business type + specialization
- Description, accessibility notes, opening times
- Inside/outside photos
- Contact information (email/phone)

### Assessment System

- Official volunteer-conducted ratings
- Admin approval workflow
- PDF reports and detailed notes
- 3-year re-assessment cycle (£30 fee)

### Public Feedback

- eBay-style sentiment rating
- Optional comments and photos
- Moderation system for content quality

### QR Sticker System

- 5 different sticker designs (by rating)
- Unique business registration ID
- Two sticker types (front-stick vs back-stick)
- Links to public business profile

### User Features

- JWT-based authentication
- Personal favorites and sharing
- Multilingual support (tourist-friendly)
- Geographic search capabilities

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
- **Geographic Integration**: PostGIS for location-based searches

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

- **Geographic Search**: PostGIS radius queries
- **Advanced Moderation**: AI-assisted review filtering
- **Mobile App**: Native iOS/Android applications
- **Integration**: Google Maps, accessibility databases
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

**Current Phase**: System design and architecture planning  
**Next Steps**: Core model implementation and API development  
**Goal**: Working MVP for proof-of-concept and potential funding

## 🗓️ Development Phases

### **Phase 1: MVP Core (4-6 weeks)**
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
- ✅ React app setup with routing
- ✅ Business listing page
- ✅ Business detail page with QR code
- ✅ Basic responsive design
- ✅ API integration with Django backend

**Success Criteria:**
- Admin can add businesses via Django admin
- Public can view business list and details
- QR codes generate and link to business pages
- System works on desktop and mobile browsers

### **Phase 2: User Features (3-4 weeks)**
**Goal**: Add public user engagement and basic business owner features

**New Features:**
- ✅ JWT authentication system
- ✅ Public user registration and login
- ✅ Business owner account type
- ✅ Business claiming process
- ✅ Basic review system (positive/neutral/negative)
- ✅ Photo upload for businesses (single image)
- ✅ User favorites system

**Enhanced Features:**
- ✅ Improved business detail pages
- ✅ User dashboard
- ✅ Basic search functionality

### **Phase 3: Assessment Workflow (3-4 weeks)**
**Goal**: Implement official assessment and approval system

**New Features:**
- ✅ Volunteer/assessor user role
- ✅ Assessment creation and submission
- ✅ Admin approval workflow
- ✅ Assessment history tracking
- ✅ Email notifications for assessments
- ✅ Basic PDF report generation

**Enhanced Features:**
- ✅ Improved admin dashboard
- ✅ Assessment scheduling system
- ✅ Business owner assessment requests

### **Phase 4: Polish & Scale (2-3 weeks)**
**Goal**: Production-ready system with enhanced features

**New Features:**
- ✅ Geographic search with PostGIS
- ✅ Advanced filtering and sorting
- ✅ Image optimization and multiple photos
- ✅ Sticker request and tracking system
- ✅ Review moderation system
- ✅ Basic analytics dashboard

**Technical Improvements:**
- ✅ Redis caching for performance
- ✅ Docker containerization
- ✅ CI/CD pipeline setup
- ✅ Error monitoring and logging
- ✅ API documentation

### **Phase 5: Production Launch (2-3 weeks)**
**Goal**: Live system ready for real users

**Launch Preparation:**
- ✅ Production deployment setup
- ✅ Domain and SSL configuration
- ✅ Database backup and recovery
- ✅ User acceptance testing
- ✅ Content management system
- ✅ Legal pages (privacy policy, terms)

**Post-Launch:**
- ✅ User feedback collection
- ✅ Performance monitoring
- ✅ Bug fixes and improvements
- ✅ Feature prioritization based on usage

### **Future Phases (Post-Launch)**

**Phase 6: Advanced Features**
- Mobile app development
- Advanced analytics and reporting
- Integration with external accessibility databases
- Multi-language support
- Advanced search with filters

**Phase 7: Business Growth**
- Business dashboard with insights
- Automated assessment reminders
- Bulk sticker ordering system
- API for third-party integrations
- White-label solutions for local councils

---

**Total MVP Timeline**: 12-16 weeks to production-ready system  
**Minimum Viable Timeline**: 4-6 weeks for proof-of-concept

*This project aims to make physical spaces more accessible for everyone while supporting businesses in their inclusivity journey.*
