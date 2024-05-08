-- Creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and stores the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_score FLOAT;
    
    -- Calculate total weighted score and total weight
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Compute weighted average score
    IF total_weight > 0 THEN
        SET weighted_score = total_score / total_weight;
    ELSE
        SET weighted_score = 0;
    END IF;
    
    -- Update user's average score
    UPDATE users
    SET average_score = weighted_score
    WHERE id = user_id;
    
END$$
DELIMITER ;
