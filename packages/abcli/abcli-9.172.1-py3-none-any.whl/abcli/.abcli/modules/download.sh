#! /usr/bin/env bash

function abcli_download() {
    local options=$1
    local open_options=$3

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        options="filename=<filename>"
        open_options="open,QGIS"
        abcli_show_usage "@download$ABCUL[$options]$ABCUL[.|<object-name>]$ABCUL[$open_options]" \
            "download object."
        return
    fi

    local filename=$(abcli_option "$options" filename)

    local object_name=$(abcli_clarify_object $2 .)
    local object_path=$abcli_object_root/$object_name

    if [ -f "../$object_name.tar.gz" ]; then
        abcli_log "✅ $object_name.tar.gz already exists - skipping download."
        return 1
    fi

    if [ ! -z "$filename" ]; then
        abcli_log "downloading $object_name/$filename ..."
        aws s3 cp "$abcli_s3_object_prefix/$object_name/$filename" "$object_path/$filename"
    else
        local exists=$(aws s3 ls $abcli_aws_s3_bucket_name/$abcli_aws_s3_prefix/$object_name.tar.gz)
        if [ -z "$exists" ]; then
            abcli_log "downloading $object_name: open ..."

            aws s3 sync "$abcli_s3_object_prefix/$object_name" "$object_path"
        else
            abcli_log "downloading $object_name: solid ..."

            pushd $abcli_object_root >/dev/null

            aws s3 cp "$abcli_s3_object_prefix/$object_name.tar.gz" .

            abcli_log "$object_name download completed - $(abcli_file size $object_name.tar.gz)"

            tar -xvf "$object_name.tar.gz"

            popd >/dev/null
        fi

    fi

    abcli_log "@download completed: $object_name $filename"

    local do_open=$(abcli_option_int "$open_options" open 0)
    [[ "$do_open" == 1 ]] &&
        abcli_open filename=$filename,$open_options \
            $object_name

    return 0

}
