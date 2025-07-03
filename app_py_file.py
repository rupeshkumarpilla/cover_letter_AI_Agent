import streamlit as st
import datetime
import io

def get_experience_text(experience):
    """Convert experience level to descriptive text"""
    experience_map = {
        'entry': 'As a motivated professional beginning my career, ',
        'mid': 'With several years of progressive experience in my field, ',
        'senior': 'As a seasoned professional with extensive experience, ',
        'executive': 'With over a decade of leadership experience, ',
        '': 'With my professional background, '
    }
    return experience_map.get(experience, 'With my professional background, ')

def create_cover_letter(data):
    """Generate a personalized cover letter based on user input"""
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    experience_text = get_experience_text(data.get('experience', ''))
    skills_text = f"My technical expertise includes {data['skills'].lower()}, " if data['skills'] else ''
    achievement_text = f"\n\nSome of my notable achievements include:\n{data['achievements']}" if data['achievements'] else ''
    motivation_text = f"\n\nI am particularly drawn to this opportunity because {data['motivation'].lower()}" if data['motivation'] else ''
    job_desc_text = "After carefully reviewing the job description, I believe my experience aligns perfectly with your requirements. " if data['job_description'] else ''
    
    cover_letter = f"""{data['full_name']}
{data['email']}{f"\n{data['phone']}" if data['phone'] else ''}

{current_date}

Dear Hiring Manager,

I am writing to express my strong interest in the {data['job_title']} position at {data['company_name']}. {experience_text}{skills_text}I am confident that my background and passion for excellence make me an ideal candidate for this role.

{job_desc_text}My professional journey has equipped me with the skills and knowledge necessary to contribute effectively to your team from day one.{achievement_text}{motivation_text}

I am excited about the opportunity to bring my unique perspective and proven track record to {data['company_name']}. I would welcome the chance to discuss how my experience and enthusiasm can contribute to your team's continued success.

Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
{data['full_name']}"""
    
    return cover_letter

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="🤖 AI Cover Letter Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #333;
        border-bottom: 2px solid #4facfe;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .tips-box {
        background: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4facfe;
        margin-top: 1rem;
    }
    .cover-letter-output {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Cover Letter Agent</h1>
        <p>Generate professional cover letters tailored to your job applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">📋 Job Information</h2>', unsafe_allow_html=True)
        job_title = st.text_input("Job Title *", placeholder="e.g., Software Engineer, Marketing Manager")
        company_name = st.text_input("Company Name *", placeholder="e.g., Google, Microsoft")
        job_description = st.text_area(
            "Job Description", 
            placeholder="Paste the job description here for a more tailored cover letter...",
            height=100
        )
        
        st.markdown('<h2 class="section-header">👤 Personal Information</h2>', unsafe_allow_html=True)
        full_name = st.text_input("Full Name *", placeholder="Your full name")
        email = st.text_input("Email *", placeholder="your.email@example.com")
        phone = st.text_input("Phone Number", placeholder="Your phone number")
        experience = st.selectbox("Experience Level", [
            "", 
            "Entry Level (0-2 years)", 
            "Mid Level (3-5 years)", 
            "Senior Level (6-10 years)", 
            "Executive Level (10+ years)"
        ])
        
        st.markdown('<h2 class="section-header">💼 Professional Background</h2>', unsafe_allow_html=True)
        skills = st.text_area(
            "Key Skills", 
            placeholder="List your relevant skills (e.g., JavaScript, Project Management, Data Analysis)",
            height=80
        )
        achievements = st.text_area(
            "Notable Achievements", 
            placeholder="Describe 2-3 key achievements or projects that demonstrate your value",
            height=100
        )
        motivation = st.text_area(
            "Why This Role?", 
            placeholder="What interests you about this specific role and company?",
            height=80
        )
    
    with col2:
        # Generate button
        if st.button("✨ Generate Cover Letter", type="primary", use_container_width=True):
            if not all([job_title, company_name, full_name, email]):
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                with st.spinner("🔄 Crafting your personalized cover letter..."):
                    # Parse experience level
                    exp_level = experience.split()[0].lower() if experience else ''
                    
                    # Create data dictionary
                    data = {
                        'job_title': job_title,
                        'company_name': company_name,
                        'job_description': job_description,
                        'full_name': full_name,
                        'email': email,
                        'phone': phone,
                        'experience': exp_level,
                        'skills': skills,
                        'achievements': achievements,
                        'motivation': motivation
                    }
                    
                    # Generate cover letter
                    cover_letter = create_cover_letter(data)
                    
                    # Store in session state
                    st.session_state.cover_letter = cover_letter
                    st.session_state.filename = f"Cover_Letter_{job_title.replace(' ', '_')}_{company_name.replace(' ', '_')}"
                    
                    st.success("✅ Cover letter generated successfully!")
        
        # Display generated cover letter
        if hasattr(st.session_state, 'cover_letter'):
            st.markdown('<h2 class="section-header">📄 Generated Cover Letter</h2>', unsafe_allow_html=True)
            
            # Display the cover letter in a nice formatted box
            st.markdown(f'<div class="cover-letter-output">{st.session_state.cover_letter}</div>', unsafe_allow_html=True)
            
            # Download buttons
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                st.download_button(
                    label="💾 Download as Text",
                    data=st.session_state.cover_letter,
                    file_name=f"{st.session_state.filename}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_btn2:
                # Create HTML version for better formatting
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Cover Letter</title>
                    <style>
                        body {{ 
                            font-family: 'Georgia', serif; 
                            line-height: 1.6; 
                            padding: 40px; 
                            max-width: 800px; 
                            margin: 0 auto;
                        }}
                        .letter {{ 
                            white-space: pre-wrap; 
                        }}
                    </style>
                </head>
                <body>
                    <div class="letter">{st.session_state.cover_letter}</div>
                </body>
                </html>
                """
                
                st.download_button(
                    label="📄 Download as HTML",
                    data=html_content,
                    file_name=f"{st.session_state.filename}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            # Copy to clipboard functionality
            st.markdown("""
            <script>
            function copyToClipboard() {
                navigator.clipboard.writeText(document.querySelector('.cover-letter-output').innerText);
                alert('Cover letter copied to clipboard!');
            }
            </script>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.info("💡 Use Ctrl+C (or Cmd+C on Mac) to copy the cover letter text above!")
        
        # Tips section
        st.markdown("""
        <div class="tips-box">
            <h3>💡 Tips for Better Cover Letters</h3>
            <ul>
                <li>✅ Include specific details from the job description</li>
                <li>📊 Quantify your achievements with numbers when possible</li>
                <li>🔍 Research the company and mention why you want to work there</li>
                <li>📝 Keep it concise - typically one page</li>
                <li>🔍 Proofread carefully before sending</li>
                <li>🎯 Customize for each application</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit | "
        "<a href='https://huggingface.co/spaces' target='_blank'>Powered by Hugging Face Spaces</a>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()