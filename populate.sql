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

INSERT INTO Department (DepartmentName)
VALUES 
    ('IT'),
    ('Marketing'),
    ('Finance'),
    ('Human Resources'),
    ('Research and Development'),
    ('Customer Support');

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


INSERT INTO Users (Name, Email, Password, RoleID, DepartmentID)
VALUES 
('John Doe', 'john.doe@example.com', 'password123', 1, 1),
('Jane Smith', 'jane.smith@example.com', 'password123', 2, 2),
('Alice Johnson', 'alice.johnson@example.com', 'password123', 3, 3),
('Bob Brown', 'bob.brown@example.com', 'password123', 4, 4);


INSERT INTO Project (ProjectName, Description, EndDate, ManagerID, ClientID)
VALUES 
('Website Redesign', 'Complete overhaul of the company website', '2024-06-30', 1, 1),
('Social Media Campaign', 'Launching a new social media marketing campaign', '2023-12-31', 1, 2),
('Product Launch', 'Introducing new product line', '2024-09-30', 1, 3);


INSERT INTO Task (TaskName, Description, EndDate, StatusID, ProjectID, AssigneeID)
VALUES 
('Design Website Layout', 'Create the layout for the new website', '2023-06-15', 2, 1, 1),
('Develop Marketing Content', 'Develop content for social media posts', '2023-05-20', 1, 2, 2),
('Quality Assurance Testing', 'Test the new product for quality assurance', '2024-05-30', 3, 3, 3);


INSERT INTO Report (ReportName, Description, Date, ProjectID)
VALUES 
('Website Design Review', 'Initial review of the website redesign project', '2023-01-15', 1),
('Marketing Campaign Analysis', 'Analysis of the social media campaign performance', '2023-04-10', 2),
('Product Testing Feedback', 'Feedback on the product testing phase', '2024-02-20', 3);
