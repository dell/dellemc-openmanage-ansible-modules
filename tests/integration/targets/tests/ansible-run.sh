#!/bin/bash

for f in \
    import_with_import_buffer-11775 \

    
do
    echo "************** Running $f.yaml *********************"
    ansible-test network-integration idrac_server_config_profile --testcase $f -vvv | tee $f.17g4log
    echo
done

# echo "************** Running $f.yaml *********************"
# ansible-test network-integration idrac_secure_boot --testcase $f | tee "logs_16g/${f}.log"
# echo


# Ran on 17G and successfully completed
# export_cifs-11763
# export_http-11764
# export_https-11765
# export_local-11761 \
# export_nfs-11762 \
# invalid_custom_default-11779 \
# invalid_export-11772 
# invalid_import-11773 \
# invalid_preview-11776 \
# valid_custom_default-11778 \
# import_cifs-11768 \
# import_http-11769 \
# import_https-11770 \
# import_nfs-11767 
# import_local-11766 \
# preview_file-11777 \
# preview_with_import_buffer-11774 \
