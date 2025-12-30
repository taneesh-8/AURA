# 🏦 AURA - AI Unified Risk & Loan Origination Assistant

**Professional Credit Decisioning Platform**

A comprehensive, enterprise-grade loan origination and risk assessment system powered by AI and machine learning.

---

## ✨ Features

### Core Functionality
- 🔐 **Multi-Role Authentication** - Admin, Manager, and Analyst roles with different permissions
- 🔍 **AI Risk Analysis** - Intelligent credit risk scoring and assessment
- 📄 **Term Sheet Generation** - Automated loan term structuring with AI explanations
- 📈 **Financial Ratio Calculator** - DSCR, Leverage Ratio, Interest Coverage analysis
- 📤 **Document Management** - Upload and track financial statements
- 🔄 **Approval Workflow** - Submit, review, approve/reject loan applications
- 📋 **Audit Trail** - Complete activity logging and compliance tracking
- 📊 **Analytics Dashboard** - Real-time insights and portfolio visualization

### Advanced Features
- 🤖 **LLM Integration** - OpenAI-powered explanations and reasoning
- 📑 **Professional PDF Generation** - Bank-grade term sheet documents
- 📈 **Interactive Charts** - Plotly-based data visualizations
- 🎨 **Modern UI/UX** - Clean, professional interface
- 🔒 **Role-Based Access Control** - Secure, permission-based features

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) OpenAI API key for LLM features

### Installation

1. **Clone or Download the Project**
```bash
cd AURA-Professional
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables (Optional)**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

5. **Create Data Directory**
```bash
mkdir data
```

6. **Run the Application**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 👤 Demo Credentials

### Admin Access (Full Permissions)
- **Username:** `admin`
- **Password:** `admin123`

### Analyst Access (Risk Analysis & Submission)
- **Username:** `analyst`
- **Password:** `risk123`

### Manager Access (Approval Authority)
- **Username:** `manager`
- **Password:** `manager123`

---

## 📁 Project Structure

```
AURA-Professional/
│
├── app.py                          # Main application entry
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
│
├── pages/                         # Streamlit multi-page app
│   ├── 1_🏠_Home.py
│   ├── 2_📊_Dashboard.py
│   ├── 3_🔍_Risk_Analysis.py
│   ├── 4_📄_Term_Sheet.py
│   ├── 5_📈_Financial_Ratios.py
│   ├── 6_📤_Document_Upload.py
│   ├── 7_🔄_Approval_Workflow.py
│   └── 8_📋_Audit_Log.py
│
├── auth/                          # Authentication module
│   ├── __init__.py
│   ├── login.py
│   └── users.py
│
├── services/                      # Business logic
│   ├── __init__.py
│   ├── risk_engine.py            # Risk scoring algorithm
│   ├── term_generator.py         # Loan term structuring
│   ├── financial_calculator.py   # Financial ratio calculations
│   ├── llm_integration.py        # OpenAI integration
│   ├── pdf_generator.py          # PDF term sheet generation
│   └── explanation_engine.py     # AI explanation generation
│
├── utils/                         # Helper functions
│   ├── __init__.py
│   ├── helpers.py                # General utilities
│   └── validators.py             # Input validation
│
├── data/                          # Data storage (JSON files)
│   ├── audit_log.json
│   └── pending_approvals.json
│
└── assets/                        # Static assets
    ├── logo.png
    └── styles.css
```

---

## 🎯 Usage Guide

### 1. Risk Analysis
1. Login with appropriate credentials
2. Navigate to **Risk Analysis** page
3. Enter company information
4. Click **Analyze Risk**
5. Review risk score and factors

### 2. Generate Term Sheet
1. Complete risk analysis first
2. Navigate to **Term Sheet** page
3. Customize terms if needed
4. Click **Generate Term Sheet**
5. Download PDF or TXT format

### 3. Financial Ratios
1. Navigate to **Financial Ratios** page
2. Enter financial metrics (EBITDA, debt, etc.)
3. Click **Calculate Ratios**
4. Review DSCR, Leverage, and Interest Coverage

### 4. Approval Workflow
**For Analysts:**
- Submit completed risk analyses for approval

**For Admins/Managers:**
- Review pending applications
- Approve, reject, or request additional information
- Add reviewer comments

### 5. Audit Trail
- View all system activities
- Filter by user, action, or date
- Export logs as JSON or CSV

---

## 🔧 Configuration

### OpenAI Integration (Optional)
To enable AI-powered explanations:

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Add to `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

**Note:** The system works without OpenAI using rule-based logic. LLM features enhance explanations but are not required.

---

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin your-github-repo-url
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Click "Deploy"

3. **Add Secrets** (if using OpenAI)
   - In Streamlit Cloud dashboard, go to Settings
   - Add secrets:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```

### Deploy to Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/Azure/GCP
Use Docker for containerized deployment:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Login with all three user roles
- [ ] Complete risk analysis workflow
- [ ] Generate and download term sheet
- [ ] Calculate financial ratios
- [ ] Upload documents
- [ ] Submit and approve loan application
- [ ] View audit log
- [ ] Test export features

---

## 📊 Technical Stack

- **Frontend:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **PDF Generation:** ReportLab
- **AI/ML:** OpenAI GPT-4 (optional)
- **Data:** Pandas, NumPy
- **Storage:** JSON files (can be upgraded to SQL database)

---

## 🔒 Security Notes

⚠️ **Important Security Considerations:**

1. **Change Default Passwords** - Update passwords in `auth/users.py` before production
2. **Secure API Keys** - Never commit `.env` file to version control
3. **Use HTTPS** - Always deploy with SSL/TLS encryption
4. **Implement Database** - Replace JSON storage with encrypted database
5. **Add Session Management** - Implement proper session timeout and management
6. **Input Sanitization** - Validate all user inputs
7. **Role-Based Access** - Enforce permissions at backend level

---

## 🚀 Future Enhancements

### Planned Features
- [ ] PostgreSQL/MySQL database integration
- [ ] Email notifications for approvals
- [ ] Real-time collaboration features
- [ ] Credit bureau API integration
- [ ] Machine learning risk models
- [ ] Multi-currency support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and reporting
- [ ] Integration with loan servicing systems

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💡 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Email: support@aura-ai.com
- Documentation: [docs.aura-ai.com](https://docs.aura-ai.com)

---

## 🙏 Acknowledgments

- Streamlit team for amazing framework
- OpenAI for GPT API
- Plotly for interactive charts
- ReportLab for PDF generation

---

## 📸 Screenshots

### Login Page
Professional authentication with role-based access

### Dashboard
Real-time analytics and portfolio insights

### Risk Analysis
AI-powered credit risk assessment

### Term Sheet Generator
Automated loan structuring with explanations

### Approval Workflow
Complete review and approval process

---

**Built with ❤️ by AURA Team**

*Version 2.0 - December 2024*