CREATE TABLE test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value INT NOT NULL
);

INSERT INTO test_table (name, value) VALUES ('Sample1', 10);
INSERT INTO test_table (name, value) VALUES ('Sample2', 20);
INSERT INTO test_table (name, value) VALUES ('Sample3', 30);
