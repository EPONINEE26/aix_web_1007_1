select * from member;
commit;

SELECT COUNT(*) FROM member;
SELECT owner, table_name FROM all_tables WHERE UPPER(table_name) = 'MEMBER';

