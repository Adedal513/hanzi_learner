CREATE TABLE hanzi (
    id SERIAL PRIMARY KEY,
    character VARCHAR(1) UNIQUE NOT NULL,
    pinyin VARCHAR(50) NOT NULL,
    meaning VARCHAR(100) NOT NULL,
    s3_image_key VARCHAR(200) NOT NULL
);

INSERT INTO hanzi (character, pinyin, meaning, s3_image_key)
VALUES 
    ('好', 'hao3', 'Хороший/Хорошо', 'hanzi/好.png'),
    ('爱', 'ai4', 'Любить', 'hanzi/爱.png'),
    ('你', 'ni3', 'Ты', 'hanzi/你.png'),
    ('哥哥', 'ge4ge5', 'Старший брат', 'hanzi/哥哥.png')
ON CONFLICT DO NOTHING;