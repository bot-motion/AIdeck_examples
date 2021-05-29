/openocd-esp32/bin/openocd -f interface/ftdi/olimex-arm-usb-tiny-h.cfg -f board/esp-wroom-32.cfg -c "program_esp32 build/partitions_singleapp.bin 0x8000 verify" -c "program_esp32 build/bootloader/bootloader.bin 0x1000 verify" -c "program_esp32 build/ai-deck-jpeg-streamer-demo.bin 0x10000 verify reset exit"

