/*
Nthras Product ERP System Database Schema
This schema is optimized for MySQL, focusing on performance, scalability, and data integrity for an Enterprise Resource Planning system. It includes comprehensive structures for managing companies, branches, users, roles, permissions, and other essential entities.

--- Recommendations for Developers ---

1. Indexing:
   - Always ensure to index foreign keys and columns frequently used in WHERE clauses, JOIN conditions, or as part of a foreign key relationship to enhance query performance.
   - Consider creating composite indexes for queries that span multiple columns frequently.

2. Data Types:
   - Choose the most appropriate data types for each column to optimize storage and performance. For instance, use INT UNSIGNED for identifiers, ENUM for columns with a limited set of predefined values, and appropriate VARCHAR lengths.
   - Use DECIMAL for precise arithmetic operations, especially for financial data.

3. Security:
   - Sensitive data such as passwords should be stored securely. Use hashing algorithms like bcrypt for passwords. Avoid storing plain-text passwords.
   - Consider field-level encryption for highly sensitive data like personal identification numbers or financial information.

4. Large Objects:
   - For large binary objects (BLOBs), such as images or documents, prefer storing them in an external storage solution (e.g., AWS S3) and save the reference URL in the database. This approach keeps the database size manageable and improves performance.

5. Data Integrity:
   - Use foreign key constraints to enforce relational integrity across tables.
   - Utilize transaction controls to ensure data consistency, particularly for operations that span multiple tables.

6. Normalization:
   - Adhere to normalization principles to reduce data redundancy and ensure data integrity. However, be mindful of over-normalization, which can lead to complex queries and affect performance.

7. Performance Optimization:
   - Use EXPLAIN to analyze and optimize query performance.
   - Consider partitioning large tables to improve query performance and management.

8. Auditing:
   - Include `created_at` and `updated_at` timestamps in all tables to track data creation and modifications.
   - Implement soft deletion (`is_deleted`) to maintain historical data without permanently removing records from the database.

9. Application-Level Considerations:
   - Where possible, offload data processing and business logic to the application level to leverage application caching and reduce database load.
   - Regularly review and optimize SQL queries used by the application, especially those that are executed frequently or involve large datasets.

10. Database Maintenance:
    - Regularly perform database maintenance tasks such as analyzing tables, optimizing indexes, and cleaning up unused data or tables to ensure optimal performance.
    - Plan for regular backups and establish a robust disaster recovery plan to safeguard your data.

By following these best practices, developers can ensure that the database layer of the Nthras Product ERP system remains robust, performant, and scalable to support the evolving needs of the business.

*/

/* Category Table */
-- Stores all categories info
CREATE TABLE categories (
    category_id CHAR(36) PRIMARY KEY, -- UUID for primary key
    category_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
/* Product Table */
-- Stores all products info
CREATE TABLE products (
    product_id CHAR(36) PRIMARY KEY, -- UUID for primary key
    product_name VARCHAR(100) NOT NULL,
    category_id CHAR(36),
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    product_image VARCHAR(255), -- Path to the product image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);



