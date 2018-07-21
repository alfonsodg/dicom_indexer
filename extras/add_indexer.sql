CREATE TABLE IF NOT EXISTS study_service (
  study_pk          INT,
  PRIMARY KEY (study_pk)
);

delimiter $$
CREATE TRIGGER indexer_process
AFTER insert ON study
FOR EACH ROW
BEGIN
insert into pacsdb.study_service values ( NEW.pk);
END $$
delimiter ;