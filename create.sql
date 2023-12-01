Create Database Project;
GO

USE Project;
GO
-- Creating Role table
CREATE TABLE Role (
    RoleID INT PRIMARY KEY IDENTITY,
    RoleName NVARCHAR(255)
);

-- Creating Department table
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY IDENTITY,
    DepartmentName NVARCHAR(255)
);

-- Creating Users table with a surrogate key
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(255),
    Email NVARCHAR(255),
    Password NVARCHAR(255),
    RoleID INT,
    DepartmentID INT,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Creating Client table
CREATE TABLE Client (
    ClientID INT PRIMARY KEY IDENTITY,
    ClientName NVARCHAR(255),
    ContactPerson NVARCHAR(255),
    Email NVARCHAR(255),
    Phone NVARCHAR(20)
);

-- Creating Project table
CREATE TABLE Project (
    ProjectID INT PRIMARY KEY IDENTITY,
    ProjectName NVARCHAR(255),
    Description TEXT,
    StartDate DATE DEFAULT GETDATE(),
    EndDate DATE,
    ManagerID INT,
    ClientID INT,
    FOREIGN KEY (ManagerID) REFERENCES Users(UserID),
    FOREIGN KEY (ClientID) REFERENCES Client(ClientID)
);

-- Creating TaskStatus table
CREATE TABLE TaskStatus (
    StatusID INT PRIMARY KEY,
    StatusName NVARCHAR(50)
);

-- Creating Task table with TaskStatus as a reference
CREATE TABLE Task (
    TaskID INT PRIMARY KEY IDENTITY,
    TaskName NVARCHAR(255),
    Description TEXT,
    StartDate DATE DEFAULT GETDATE(),
    EndDate DATE,
    StatusID INT,
    ProjectID INT,
    AssigneeID INT,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID),
    FOREIGN KEY (AssigneeID) REFERENCES Users(UserID),
    FOREIGN KEY (StatusID) REFERENCES TaskStatus(StatusID)
);

-- Creating Report table
CREATE TABLE Report (
    ReportID INT PRIMARY KEY IDENTITY,
    ReportName NVARCHAR(255),
    Description TEXT,
    Date DATE,
    ProjectID INT,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
);