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


/*select patient.pk patient_pk,patient.pat_id patient_id,patient.pat_name patient_name,study.pk study_pk,study.study_iuid,study.study_datetime,study.study_desc study_description,study.mods_in_study study_modality,study.num_series study_series,study.num_instances study_instances from patient left join study on study.patient_fk=patient.pk inner join study_service on study_service.study_pk=study.pk*/
