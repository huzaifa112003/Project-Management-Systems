INSERT INTO Department (DepartmentName)
VALUES 
    ('IT'),
    ('Marketing'),
    ('Finance'),
    ('Human Resources'),
    ('Research and Development'),
    ('Customer Support');

-- Inserting data into the Role table with additional roles
INSERT INTO Role (RoleName)
VALUES 
    ('Brand Strategist'),
    ('Social Media Coordinator'),
    ('Public Relations Specialist'),
    ('Content Writer'),
    ('SEO Specialist'),
    ('User Experience Designer'),
    ('Front-End Developer'),
    ('Back-End Developer'),
    ('Database Administrator'),
    ('Network Engineer'),
    ('Cybersecurity Analyst'),
    ('Business Analyst'),
    ('Financial Analyst'),
    ('Risk Manager'),
    ('Compliance Officer'),
    ('Procurement Manager'),
    ('Logistics Coordinator'),
    ('Product Designer'),
    ('Event Planner'),
    ('Corporate Trainer'),
    ('Recruitment Specialist'),
    ('Payroll Administrator'),
    ('Environmental Health and Safety Officer'),
    ('Research Scientist'),
    ('Technical Support Engineer');


INSERT INTO TaskStatus (StatusID, StatusName)
VALUES 
    (1, 'Not Started'),
    (2, 'In Progress'),
    (3, 'Completed'),
    (4, 'On Hold'),
    (5, 'Cancelled');


INSERT INTO Client (ClientName, ContactPerson, Email, Phone)
VALUES 
    ('ABC Corporation', 'John Smith', 'john.smith@abc.com', '123-456-7890'),
    ('XYZ Ltd', 'Jane Doe', 'jane.doe@xyz.com', '987-654-3210'),
    ('Acme Industries', 'Bob Johnson', 'bob.johnson@acme.com', '555-123-4567'),
    ('Tech Solutions', 'Alice Williams', 'alice.williams@techsolutions.com', '888-777-6666'),
    ('Global Ventures', 'Charlie Brown', 'charlie.brown@globalventures.com', '444-333-2222');

