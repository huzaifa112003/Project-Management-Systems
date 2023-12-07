# Project-Management-Systems
This Project Management Tool is a desktop application designed to help teams manage tasks, projects and monitor them efficiently. Built with PyQt for the frontend and Python with a Microsoft SQL Server backend, it provides an interactive user interface for managing project workflows, task assignments, and status updates.

## Features
- Task management: Create, assign, and update tasks with status tracking.
- Project oversight: View and manage project details including timelines and associated clients.
- Reporting: Generate concise reports on project progress and task completion.
- User and role management: Handle user accounts with different roles and permissions.

## Important Note
The manager with the primary id 1 John Doe has all the admin access who can create, edit and delete projects and tasks. Rest of the users do not have admin access, hence they can only view projects and tasks. You can change admin controls as per your need.

## ERD Overview
The Entity-Relationship Diagram (ERD) provides a visual representation of the database schema used by the application, including tables for Users, Roles, Departments, Tasks, Projects, Clients, and Reports.

## Prerequisites
To run this application, you'll need:
- Python (3.x recommended)
- PyQt5 or PyQt6
- pyodbc
- A running instance of Microsoft SQL Server
