"""
Legal Data Explorer for the AgentVerse platform.
Allows users to browse and search public court case data.
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import random

def render_page():
    """Render the legal data explorer page"""
    st.header("📚 Legal Data Explorer")
    
    st.markdown("""
    Browse and search through our collection of public court case data. 
    This dataset can be used to train and test AI agents for legal tasks, 
    particularly for defense preparation.
    """)
    
    # Sample data - in a real app, this would come from a database
    case_data = generate_sample_cases()
    
    # Left sidebar for navigation and filters
    st.sidebar.markdown("### Filters")
    
    # Case type filter
    case_types = ["All Types", "Criminal", "Civil", "Bankruptcy", "Family", "Immigration"]
    selected_type = st.sidebar.selectbox("Case Type", case_types)
    
    # Jurisdiction filter
    jurisdictions = ["All Jurisdictions", "Federal", "State - NY", "State - CA", "State - TX", "State - FL"]
    selected_jurisdiction = st.sidebar.selectbox("Jurisdiction", jurisdictions)
    
    # Date range filter
    st.sidebar.markdown("### Date Range")
    start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365*2))
    end_date = st.sidebar.date_input("End Date", datetime.now())
    
    # Full text search
    search_query = st.text_input("🔍 Search cases and documents", placeholder="Search by keywords, case number, party name, etc.")
    
    # Apply filters
    filtered_cases = case_data
    if selected_type != "All Types":
        filtered_cases = [case for case in filtered_cases if case["type"] == selected_type]
    if selected_jurisdiction != "All Jurisdictions":
        filtered_cases = [case for case in filtered_cases if case["jurisdiction"] == selected_jurisdiction]
        
    # Apply search if provided
    if search_query:
        search_query = search_query.lower()
        filtered_cases = [
            case for case in filtered_cases if 
            search_query in case["name"].lower() or
            search_query in case["case_number"].lower() or
            search_query in case["description"].lower() or
            any(search_query in doc["title"].lower() for doc in case["documents"])
        ]
    
    # Display number of results
    st.markdown(f"### Found {len(filtered_cases)} cases")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["List View", "Card View"])
    
    with tab1:
        # Create a DataFrame for the table view
        if filtered_cases:
            df = pd.DataFrame([
                {
                    "Case Name": case["name"],
                    "Case Number": case["case_number"],
                    "Type": case["type"],
                    "Jurisdiction": case["jurisdiction"],
                    "Filing Date": case["filing_date"],
                    "Status": case["status"],
                    "Documents": len(case["documents"])
                } for case in filtered_cases
            ])
            
            # Display the table with a callback for row selection
            selected_indices = st.dataframe(
                df, 
                use_container_width=True,
                column_config={
                    "Case Name": st.column_config.TextColumn("Case Name", width="large"),
                    "Documents": st.column_config.NumberColumn("Documents", format="%d")
                }
            )
        else:
            st.info("No cases match your search criteria. Try adjusting your filters.")
    
    with tab2:
        # Display as cards
        if filtered_cases:
            # Split into columns for card view
            cols = st.columns(2)
            for i, case in enumerate(filtered_cases):
                with cols[i % 2]:
                    with st.container():
                        st.markdown(f"""
                        <div style='padding: 15px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 10px;'>
                            <h3 style='margin: 0 0 10px 0; color: #2c3e50;'>{case['name']}</h3>
                            <p style='margin: 0; color: #7f8c8d; font-size: 0.8em;'>{case['case_number']} | {case['jurisdiction']} | {case['type']}</p>
                            <p style='margin: 10px 0; font-size: 0.9em;'>{case['description'][:150]}...</p>
                            <div style='display: flex; justify-content: space-between; font-size: 0.8em;'>
                                <span>Filed: {case['filing_date']}</span>
                                <span>Status: {case['status']}</span>
                                <span>Documents: {len(case['documents'])}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No cases match your search criteria. Try adjusting your filters.")
    
    # Case viewer section
    st.markdown("---")
    st.markdown("### Case Viewer")
    
    # Select case for viewing
    if filtered_cases:
        case_options = {case["name"]: i for i, case in enumerate(filtered_cases)}
        selected_case_name = st.selectbox("Select a case to view", list(case_options.keys()))
        selected_case = filtered_cases[case_options[selected_case_name]]
        
        # Display case details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {selected_case['name']}")
            st.markdown(f"**Case Number:** {selected_case['case_number']}")
            st.markdown(f"**Description:** {selected_case['description']}")
            
            # Display parties
            st.markdown("##### Parties")
            
            parties_df = pd.DataFrame([
                {"Name": party["name"], "Role": party["role"], "Representation": party["representation"]}
                for party in selected_case["parties"]
            ])
            st.dataframe(parties_df, use_container_width=True)
            
        with col2:
            st.markdown("##### Case Information")
            st.markdown(f"**Type:** {selected_case['type']}")
            st.markdown(f"**Jurisdiction:** {selected_case['jurisdiction']}")
            st.markdown(f"**Filing Date:** {selected_case['filing_date']}")
            st.markdown(f"**Status:** {selected_case['status']}")
            st.markdown(f"**Judge:** {selected_case['judge']}")
            
            # Allow downloading case data
            if st.button("Export Case Metadata (JSON)"):
                # Convert to JSON
                case_json = json.dumps(selected_case, indent=2)
                # Provide download button
                st.download_button(
                    label="Download JSON",
                    data=case_json,
                    file_name=f"{selected_case['case_number']}.json",
                    mime="application/json"
                )
                
        # Display documents
        st.markdown("##### Case Documents")
        
        if selected_case["documents"]:
            # Create document tabs
            doc_tab_titles = [doc["title"] for doc in selected_case["documents"]]
            doc_tabs = st.tabs(doc_tab_titles)
            
            for i, (tab, doc) in enumerate(zip(doc_tabs, selected_case["documents"])):
                with tab:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Filed:** {doc['filing_date']}")
                        st.markdown(f"**Document Type:** {doc['doc_type']}")
                        st.markdown(f"**Pages:** {doc['pages']}")
                    with col2:
                        st.download_button(
                            label="Download Document",
                            data=f"Sample content for {doc['title']}",
                            file_name=f"{doc['title'].replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                    
                    # Display document preview
                    st.markdown("**Document Preview:**")
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; height: 400px; overflow-y: auto; font-family: "Courier New", monospace;'>
                        {doc['content']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Document tools
                    st.markdown("##### Analysis Tools")
                    tool_col1, tool_col2, tool_col3 = st.columns(3)
                    with tool_col1:
                        if st.button("Extract Key Facts", key=f"facts_{i}"):
                            st.info("""
                            **Key Facts Extracted:**
                            - Defendant claims to be at home during the alleged crime
                            - Witness testimony places defendant at the scene
                            - Security camera footage is inconclusive
                            - No physical evidence links defendant to crime scene
                            """)
                    with tool_col2:
                        if st.button("Find Related Cases", key=f"related_{i}"):
                            st.info("""
                            **Related Cases:**
                            - State v. Johnson (2022) - Similar fact pattern
                            - United States v. Williams (2019) - Precedent on evidence
                            - In re Garcia (2023) - Related procedural ruling
                            """)
                    with tool_col3:
                        if st.button("Suggest Defense Strategy", key=f"strategy_{i}"):
                            st.info("""
                            **Strategy Suggestions:**
                            - Challenge witness credibility
                            - Move to exclude inconclusive camera footage
                            - Emphasize lack of physical evidence
                            - Establish timeline supporting alibi
                            """)
        else:
            st.info("No documents available for this case.")
    else:
        st.info("Select a case from the list above to view details.")

def generate_sample_cases():
    """Generate sample case data for demonstration"""
    case_types = ["Criminal", "Civil", "Bankruptcy", "Family", "Immigration"]
    jurisdictions = ["Federal", "State - NY", "State - CA", "State - TX", "State - FL"]
    statuses = ["Open", "Closed", "Pending", "On Appeal", "Stayed"]
    
    # Generate a set of sample cases
    cases = []
    
    # Criminal cases
    cases.append({
        "name": "United States v. Johnson",
        "case_number": "CR-2023-1234",
        "type": "Criminal",
        "jurisdiction": "Federal",
        "filing_date": "2023-06-15",
        "status": "Open",
        "judge": "Hon. Maria Rodriguez",
        "description": "Defendant John Johnson is charged with wire fraud in connection with a scheme to defraud investors through false representations about a technology startup.",
        "parties": [
            {"name": "United States of America", "role": "Plaintiff", "representation": "US Attorney's Office"},
            {"name": "John Johnson", "role": "Defendant", "representation": "Smith & Associates"}
        ],
        "documents": [
            {
                "title": "Indictment",
                "doc_type": "Charging Document",
                "filing_date": "2023-06-15",
                "pages": 12,
                "content": """UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK
---------------------------------
UNITED STATES OF AMERICA
                                        INDICTMENT
       - against -
                                        23 CR 1234
JOHN JOHNSON,
                                        (18 U.S.C. §§ 1343, 1349)
                        Defendant.
---------------------------------

                                COUNT ONE
                            (Wire Fraud Conspiracy)

The Grand Jury charges:

1. From at least in or about January 2018 up to and including in or about December 2022, in the Southern District of New York and elsewhere, JOHN JOHNSON, the defendant, willfully and knowingly, did combine, conspire, confederate, and agree together and with others known and unknown, to commit wire fraud, in violation of Title 18, United States Code, Section 1343.

2. It was a part and an object of the conspiracy that JOHN JOHNSON, the defendant, and others known and unknown, willfully and knowingly, having devised and intending to devise a scheme and artifice to defraud, and for obtaining money and property by means of false and fraudulent pretenses, representations, and promises, would and did transmit and cause to be transmitted by means of wire, radio, and television communication in interstate and foreign commerce, writings, signs, signals, pictures, and sounds for the purpose of executing such scheme and artifice, in violation of Title 18, United States Code, Section 1343.
"""
            },
            {
                "title": "Motion to Suppress",
                "doc_type": "Motion",
                "filing_date": "2023-07-25",
                "pages": 18,
                "content": """UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK
---------------------------------
UNITED STATES OF AMERICA
                                           
       - against -                         23 CR 1234
                                           
JOHN JOHNSON,                              MOTION TO SUPPRESS
                                           
                        Defendant.
---------------------------------

MOTION TO SUPPRESS EVIDENCE

Defendant John Johnson, by and through his attorneys, Smith & Associates, hereby moves this Court for an order suppressing all evidence obtained from the search of his residence located at 123 Main Street, New York, NY, on April 15, 2023, and all fruits thereof. The search warrant lacked probable cause, contained material misrepresentations, and was executed in an unreasonable manner in violation of Mr. Johnson's rights under the Fourth Amendment to the United States Constitution.

BACKGROUND FACTS

On April 15, 2023, agents of the Federal Bureau of Investigation executed a search warrant at Mr. Johnson's residence. The warrant purported to authorize the seizure of all electronic devices, financial records, and communications relating to TechFuture, Inc. and its investors from January 1, 2018, to the present.

The affidavit in support of the warrant relied primarily on statements from a confidential informant who had previously provided unreliable information to law enforcement and who had a financial interest in the outcome of this investigation. Moreover, the affidavit omitted material facts regarding the informant's credibility and motivation.
"""
            },
            {
                "title": "Order on Motion to Suppress",
                "doc_type": "Order",
                "filing_date": "2023-08-20",
                "pages": 8,
                "content": """UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK
---------------------------------
UNITED STATES OF AMERICA
                                           
       - against -                         23 CR 1234
                                           
JOHN JOHNSON,                              ORDER
                                           
                        Defendant.
---------------------------------

ORDER ON DEFENDANT'S MOTION TO SUPPRESS

Upon consideration of Defendant's Motion to Suppress Evidence (Dkt. 28), the Government's Opposition (Dkt. 32), and oral argument held on August 15, 2023, the Court hereby DENIES Defendant's motion.

The Court finds that the search warrant was supported by probable cause. The affidavit provided sufficient factual information from multiple sources, including the confidential informant, corroborating financial records, and electronic communications independently obtained by investigators. Although the defendant challenges the reliability of the confidential informant, the Court finds that the information provided by the informant was sufficiently corroborated by other evidence.

The Court further finds that the execution of the warrant was reasonable and within the scope authorized by the warrant. The agents conducted the search during daylight hours, provided the defendant with a copy of the warrant, and limited their seizure to items within the scope of the warrant.

Accordingly, Defendant's Motion to Suppress is DENIED.

SO ORDERED.

Dated: August 20, 2023
New York, New York

___________________________
Hon. Maria Rodriguez
United States District Judge
"""
            }
        ]
    })
    
    # Bankruptcy case
    cases.append({
        "name": "In re Smith Corporation",
        "case_number": "BK-2023-56789",
        "type": "Bankruptcy",
        "jurisdiction": "Federal",
        "filing_date": "2023-01-10",
        "status": "Open",
        "judge": "Hon. Robert Chen",
        "description": "Chapter 11 reorganization of Smith Corporation, a regional retail chain with 28 locations and approximately 350 employees.",
        "parties": [
            {"name": "Smith Corporation", "role": "Debtor", "representation": "Bankruptcy Partners LLP"},
            {"name": "First National Bank", "role": "Creditor", "representation": "Financial Law Group"},
            {"name": "Pension Benefit Guaranty Corporation", "role": "Interested Party", "representation": "In-house Counsel"}
        ],
        "documents": [
            {
                "title": "Voluntary Petition",
                "doc_type": "Petition",
                "filing_date": "2023-01-10",
                "pages": 45,
                "content": """UNITED STATES BANKRUPTCY COURT
DISTRICT OF DELAWARE
---------------------------------
In re:                                    Chapter 11
                                        
SMITH CORPORATION,                       Case No. 23-56789
                                        
                        Debtor.
---------------------------------

VOLUNTARY PETITION FOR RELIEF UNDER CHAPTER 11

Smith Corporation, a Delaware corporation with its principal place of business at 789 Retail Avenue, Wilmington, Delaware, hereby submits this voluntary petition for relief under Chapter 11 of the Bankruptcy Code.

The Debtor estimates its assets to be between $10,000,000 and $50,000,000 and its liabilities to be between $50,000,000 and $100,000,000.

The Debtor has 28 retail locations across the Mid-Atlantic region and employs approximately 350 individuals. The company has suffered significant financial distress due to the changing retail landscape, increased competition from online retailers, and the lingering effects of the COVID-19 pandemic on consumer shopping habits.

Through this Chapter 11 case, the Debtor seeks to restructure its obligations, renegotiate certain leases, and implement a revised business model that will allow it to remain competitive in the current retail environment.
"""
            },
            {
                "title": "First Day Declaration",
                "doc_type": "Declaration",
                "filing_date": "2023-01-10",
                "pages": 32,
                "content": """UNITED STATES BANKRUPTCY COURT
DISTRICT OF DELAWARE
---------------------------------
In re:                                    Chapter 11
                                        
SMITH CORPORATION,                       Case No. 23-56789
                                        
                        Debtor.
---------------------------------

DECLARATION OF JAMES SMITH IN SUPPORT OF 
CHAPTER 11 PETITION AND FIRST DAY MOTIONS

I, James Smith, declare under penalty of perjury:

1. I am the Chief Executive Officer and Chairman of the Board of Directors of Smith Corporation (the "Debtor"). I have served in this capacity since 1998 when I founded the company.

2. I submit this declaration in support of the Debtor's voluntary petition for relief under chapter 11 of title 11 of the United States Code (the "Bankruptcy Code") and the Debtor's "first day" motions identified below.

3. I am familiar with the Debtor's day-to-day operations, business affairs, and books and records. Except as otherwise indicated, all facts set forth in this Declaration are based upon my personal knowledge, my discussions with other members of the Debtor's management team and the Debtor's advisors, my review of relevant documents, or my opinion based upon my experience and knowledge of the Debtor's operations and financial condition. If called upon to testify, I would testify competently to the facts set forth in this Declaration.

COMPANY BACKGROUND

4. The Debtor was founded in 1998 as a single retail store in Wilmington, Delaware, selling mid-range home furnishings and decor. Over the next 25 years, the company expanded to 28 retail locations across Delaware, Pennsylvania, Maryland, Virginia, and New Jersey.

5. At its peak in 2018, the company generated annual revenues of approximately $75 million and employed over 500 individuals.
"""
            }
        ]
    })
    
    # Generate more random cases
    for i in range(8):
        case_type = random.choice(case_types)
        jurisdiction = random.choice(jurisdictions)
        status = random.choice(statuses)
        
        # Generate random dates within last 3 years
        days_ago = random.randint(1, 365*3)
        filing_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Create sample case names based on type
        if case_type == "Criminal":
            name = f"{'United States' if jurisdiction == 'Federal' else 'State'} v. {random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson', 'Taylor'])}"
            case_number = f"CR-{2020 + random.randint(0, 3)}-{random.randint(1000, 9999)}"
            description = f"Criminal prosecution for {random.choice(['fraud', 'theft', 'assault', 'drug possession', 'tax evasion'])}."
        elif case_type == "Civil":
            plaintiffs = random.choice(['Johnson', 'Martinez', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin'])
            defendants = random.choice(['Acme Corp', 'Metro Industries', 'First National Bank', 'City Hospital', 'Tech Solutions Inc'])
            name = f"{plaintiffs} v. {defendants}"
            case_number = f"CV-{2020 + random.randint(0, 3)}-{random.randint(1000, 9999)}"
            description = f"Civil lawsuit for {random.choice(['breach of contract', 'personal injury', 'employment discrimination', 'property damage', 'medical malpractice'])}."
        elif case_type == "Bankruptcy":
            entity = random.choice(['ABC Stores', 'Johnson Manufacturing', 'Metro Restaurants', 'Tech Innovations', 'Coastal Properties'])
            name = f"In re {entity}"
            case_number = f"BK-{2020 + random.randint(0, 3)}-{random.randint(10000, 99999)}"
            description = f"Chapter {random.choice(['7', '11', '13'])} bankruptcy proceeding."
        else:
            name = f"In the Matter of {random.choice(['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson', 'Taylor'])}"
            case_number = f"{case_type[:3].upper()}-{2020 + random.randint(0, 3)}-{random.randint(1000, 9999)}"
            description = f"{case_type} proceeding related to {random.choice(['divorce', 'child custody', 'immigration status', 'asylum', 'property division', 'adoption'])}."
        
        # Create random documents
        num_docs = random.randint(0, 5)
        documents = []
        
        doc_types = {
            "Criminal": ["Indictment", "Motion to Suppress", "Motion to Dismiss", "Plea Agreement", "Sentencing Memorandum"],
            "Civil": ["Complaint", "Answer", "Motion for Summary Judgment", "Discovery Request", "Settlement Agreement"],
            "Bankruptcy": ["Petition", "Schedules", "Plan of Reorganization", "Motion for Relief from Stay", "Disclosure Statement"],
            "Family": ["Petition for Divorce", "Custody Agreement", "Support Order", "Property Settlement", "Visitation Schedule"],
            "Immigration": ["Asylum Application", "Motion to Reopen", "Appeal Brief", "Visa Petition", "Removal Defense"]
        }
        
        for j in range(num_docs):
            doc_type = random.choice(doc_types.get(case_type, ["Motion", "Order", "Petition", "Response"]))
            doc_date = (datetime.now() - timedelta(days=random.randint(1, days_ago))).strftime("%Y-%m-%d")
            
            documents.append({
                "title": f"{doc_type} - {doc_date}",
                "doc_type": doc_type,
                "filing_date": doc_date,
                "pages": random.randint(1, 50),
                "content": f"Sample content for {doc_type} in case {case_number}. This is placeholder text for the document preview."
            })
        
        # Create random parties
        parties = []
        if case_type == "Criminal":
            parties.append({"name": "United States" if jurisdiction == "Federal" else "State", "role": "Prosecutor", "representation": "US Attorney's Office" if jurisdiction == "Federal" else "District Attorney"})
            parties.append({"name": name.split("v. ")[1], "role": "Defendant", "representation": f"{random.choice(['Smith', 'Jones', 'Martinez', 'Chan'])} & Associates"})
        elif case_type == "Civil":
            plaintiff = name.split(" v. ")[0]
            defendant = name.split(" v. ")[1]
            parties.append({"name": plaintiff, "role": "Plaintiff", "representation": f"{random.choice(['Smith', 'Jones', 'Martinez', 'Chan'])} & Associates"})
            parties.append({"name": defendant, "role": "Defendant", "representation": f"{random.choice(['Brown', 'Davis', 'Wilson', 'Taylor'])} LLP"})
        else:
            parties.append({"name": name.split("re ")[1] if "re " in name else name.split("of ")[1], "role": "Primary Party", "representation": f"{random.choice(['Legal Aid', 'Smith & Jones', 'Public Defender', 'Wilson Law Group', 'Immigration Legal Services'])}"})
        
        cases.append({
            "name": name,
            "case_number": case_number,
            "type": case_type,
            "jurisdiction": jurisdiction,
            "filing_date": filing_date,
            "status": status,
            "judge": f"Hon. {random.choice(['Smith', 'Jones', 'Martinez', 'Chan', 'Brown', 'Davis', 'Wilson', 'Taylor'])}",
            "description": description,
            "parties": parties,
            "documents": documents
        })
    
    return cases 