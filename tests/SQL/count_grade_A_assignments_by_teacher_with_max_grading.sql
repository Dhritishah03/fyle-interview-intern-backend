-- Write query tofind the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grades AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_graded,
        SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) AS grade_a_count
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
),
top_teacher AS (
    SELECT 
        teacher_id,
        MAX(total_graded) AS max_graded
    FROM 
        teacher_grades
    GROUP BY 
        teacher_id
    ORDER BY 
        max_graded DESC
    LIMIT 1
)
SELECT 
    tg.grade_a_count,
    tg.teacher_id
FROM 
    teacher_grades tg
JOIN 
    top_teacher tt
ON 
    tg.teacher_id = tt.teacher_id;

