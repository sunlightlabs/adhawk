drop table if exists reporting_youtube_import;
create table reporting_youtube_import (
    fec_id varchar(9),
    super_pac_entity varchar(100),
    youtube_channel_url varchar(100),
    profile_url varchar(100),
    org_url varchar(50),
    additional_video varchar(100),
);
