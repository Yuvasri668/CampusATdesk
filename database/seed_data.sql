-- Users
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@example.com', 'pbkdf2:sha256:260000$Ww39uDyIP4v8TjuF$59112d6ccf57c1dff3150251ff33388ef5c6157ae686cdd7d8733306ddbce36c', 'admin'),
('adminuser', 'adminuser@example.com', 'pbkdf2:sha256:260000$GVhy3ZR92ZYonChS$a352e7be2732c5f9decec1e367d72ce8e087059aecab4257fd892cad24661150', 'admin'),
('recuser', 'recuser@example.com', 'pbkdf2:sha256:260000$QkADMfD5e8FvIA1R$a564483a330696de75e79e017dda25e2b12a8c05dbd0e90d607aced3be712962', 'recruiter'),
('recruiter', 'recruiter@example.com', 'pbkdf2:sha256:260000$Ww39uDyIP4v8TjuF$59112d6ccf57c1dff3150251ff33388ef5c6157ae686cdd7d8733306ddbce36c', 'recruiter'),
('student', 'student@example.com', 'pbkdf2:sha256:260000$QkADMfD5e8FvIA1R$a564483a330696de75e79e017dda25e2b12a8c05dbd0e90d607aced3be712962', 'student'),
('student1', 'student1@example.com', 'pbkdf2:sha256:260000$Ww39uDyIP4v8TjuF$59112d6ccf57c1dff3150251ff33388ef5c6157ae686cdd7d8733306ddbce36c', 'student'),
('student2', 'student2@example.com', 'pbkdf2:sha256:260000$Ww39uDyIP4v8TjuF$59112d6ccf57c1dff3150251ff33388ef5c6157ae686cdd7d8733306ddbce36c', 'student')
ON DUPLICATE KEY UPDATE username = username;

INSERT INTO companies (name, location) VALUES
('TechCorp', 'Mumbai'),
('InnovateLabs', 'Bangalore');

UPDATE users u
INNER JOIN companies c ON c.name = 'TechCorp'
SET u.company_id = c.id
WHERE u.email IN ('recruiter@example.com', 'recuser@example.com') AND u.role = 'recruiter';

INSERT IGNORE INTO categories (name) VALUES ('IT'), ('Marketing');

INSERT INTO jobs (title, description, required_skills, location, job_type, category_id, posted_by)
SELECT 'Python Developer', 'Backend development with Python', 'Python, Flask, SQL', 'Mumbai', 'Full-time', c.id, u.id
FROM categories c, users u
WHERE c.name = 'IT' AND u.email = 'recruiter@example.com'
LIMIT 1;

INSERT INTO jobs (title, description, required_skills, location, job_type, category_id, posted_by)
SELECT 'Frontend Engineer', 'React and JavaScript development', 'React, JavaScript, CSS', 'Bangalore', 'Full-time', c.id, u.id
FROM categories c, users u
WHERE c.name = 'IT' AND u.email = 'recruiter@example.com'
LIMIT 1;

INSERT INTO jobs (title, description, required_skills, location, job_type, category_id, posted_by)
SELECT 'Marketing Specialist', 'Digital marketing and content', 'SEO, Social Media', 'Mumbai', 'Part-time', c.id, u.id
FROM categories c, users u
WHERE c.name = 'Marketing' AND u.email = 'recruiter@example.com'
LIMIT 1;

INSERT INTO applications (student_id, job_id, status)
SELECT s.id, j.id, 'Applied'
FROM users s
JOIN jobs j ON j.posted_by = (SELECT id FROM users WHERE email = 'recruiter@example.com' LIMIT 1)
WHERE s.email IN ('student1@example.com', 'student2@example.com')
  AND NOT EXISTS (
      SELECT 1
      FROM applications a
      WHERE a.student_id = s.id AND a.job_id = j.id
  );

INSERT INTO test_table (name) VALUES ('Seed Row 1');
INSERT INTO test_table (name) VALUES ('Seed Row 2');
