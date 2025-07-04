import struct


def extract_scripts_from_plugin_old(filepath):
    scripts = []
    with open(filepath, 'rb') as f:
        data = f.read()
        offset = 0

        while offset < len(data):
            if data[offset:offset+4] == b'SCPT':
                #record_size = int.from_bytes(data[offset+4:offset+8], 'little')
                record_size = struct.unpack(">HH", data[:4])
                print(record_size)
                record_data = data[offset+16 : offset+16+record_size]
                name = record_data[0:32].split(b'\x00')[0].decode('utf-8')
                script_offset = record_data.find(b'Begin')
                if script_offset != -1:
                    source = record_data[script_offset:].decode('utf-8', errors='ignore')
                    scripts.append((name, source))
                offset += 16 + record_size
            else:
                offset += 1
    return scripts




def extract_scripts_from_plugin(filepath, debug=False):
    scripts = []
    with open(filepath, 'rb') as f:
        data = f.read()
        offset = 0
        
        hdr_size = 0

        if data[offset:offset+4] == b'TES3':
            if debug: print('got tes3!')
            hdr_size = struct.unpack("<I", data[offset+4:offset+8])[0] + 16
            if debug: print(hdr_size)
            offset += hdr_size
            

            while offset < len(data):
                if data[offset:offset+4] == b'SCPT':
                    if debug: print('got scpt!')
                    record_size = struct.unpack("<I", data[offset+4:offset+8])[0] + 16
                    if debug: print(record_size)
                    
                    inner_offset = offset + 16

                    if data[inner_offset:inner_offset+4] == b'SCHD':
                        if debug: print('got subheader!')
                        #inner_offset += 4
                        subheader_size = struct.unpack("<I", data[inner_offset+4:inner_offset+8])[0] + 8
                        if debug: print(subheader_size)
                        inner_offset += subheader_size
                        if debug: print(inner_offset)

                        tag = data[inner_offset:inner_offset+4]
                        if tag == b'SCVR' or tag == b'SCDT': #skip these
                            if debug: print('got scvr or scdt!')
                            subrecord_size = struct.unpack("<I", data[inner_offset+4:inner_offset+8])[0] + 8
                            if debug: print(subrecord_size)
                            inner_offset += subrecord_size
                            if debug: print(inner_offset)
                            

                        tag = data[inner_offset:inner_offset+4]
                        if tag == b'SCVR' or tag == b'SCDT': #skip these
                            if debug: print('got scvr or scdt!')
                            subrecord_size = struct.unpack("<I", data[inner_offset+4:inner_offset+8])[0] + 8
                            if debug: print(subrecord_size)
                            inner_offset += subrecord_size
                            if debug: print(inner_offset)
                            
                            
                        if data[inner_offset:inner_offset+4] == b'SCTX':
                            if debug: print('got sctx!')
                            sctx_size = struct.unpack("<I", data[inner_offset+4:inner_offset+8])[0] + 8
                            if debug: print(sctx_size)

                            raw_bytes = data[inner_offset+8 : inner_offset + sctx_size]
                            raw_bytes = raw_bytes.replace('\r\n', '\n')
                            #decoded_script = raw_bytes.decode('utf-8', errors='ignore')  # or 'windows-1252' if needed
                            scripts.append(raw_bytes)

                            #scripts.append(data[inner_offset+8:inner_offset+sctx_size])
                            if debug: print(data[inner_offset+8])
                            if debug: print(data[inner_offset+sctx_size-1])
                            inner_offset += sctx_size
                            if debug: print(inner_offset)
                            
                    offset += record_size
                else:
                    record_size = struct.unpack("<I", data[offset+4:offset+8])[0] + 16
                    if debug: print('skipping record at ' + str(offset))
                    offset += record_size
                

        #while offset < len(data):
        #    offset += 1

    if debug: print(scripts)
    return scripts

