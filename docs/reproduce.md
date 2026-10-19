# Build and reproduce

Use a standalone Windows VM, a local SMTP capture service, an internal HTTP service and Splunk. Apply the included Sysmon configuration and enable Security process creation with command lines and PowerShell Script Block Logging.

## Delivery

Install the SMTP capture dependency and run the small local receiver:

```bash
python3 -m pip install aiosmtpd==1.4.6
python3 lab/smtp-inbox.py --output mail
```

Create `Benefits-Review.zip` containing `lab/Benefits-Review.pdf.cmd` and `lab/review.ps1`. Serve that archive at `/phishing/Benefits-Review.zip` on the isolated HTTP service. Send the sample with `lab/send-message.py` and specify the ZIP path. The receiver stores the actual accepted message bytes and computes the attachment hash from the MIME message.

The recorded service address is `10.0.2.2:8766`, the QEMU host gateway. Adjust the message URL and `review.ps1` together when using another internal topology. Keep reserved `.example` addresses for the sample messages.

## Windows review

Inspect the original message and hash its MIME attachment. Download the linked archive into a lab directory and compare its hash before extracting it. Review both source files. `Benefits-Review.pdf.cmd` is intentionally a command script with a misleading double extension; its payload only writes a local marker and contacts the internal lab service.

Record the UTC window, launch the command script inside the isolated VM and collect Sysmon 1/3/11, Security 4688 and PowerShell 4104. Preserve the original XML as well as normalized JSONL. Follow PID and ProcessGuid relationships to the output marker.

## Splunk

Install `splunk/app` as a local app. Import `evidence/events.jsonl` into index `lab_phishing` with sourcetype `soc:windows:event`. Import `evidence/smtp-deliveries.jsonl` with sourcetype `soc:smtp:delivery`.

The SMTP import has one scalar `recipient` per delivery row. The untouched original receiver log retains its recipient array. Run the six saved searches and open the Splunk dashboard views. Compare counts and UTC values with the source records rather than assuming that each delivery resulted in execution.

## Cleanup

Stop the SMTP and HTTP services. Remove the case directory under `C:\Users\Public\Documents\MohamedLab\Phishing` and the marker directory under `C:\ProgramData\MohamedLab\Phishing` after preserving the evidence. This sample does not install persistence.

## Capture helper

`lab/export-events.ps1` exports original event XML and matching normalized JSONL for a UTC window. For example: `./lab/export-events.ps1 -StartUtc $start -EndUtc $end -Output C:\MohamedLab\Evidence`. Record the UTC boundaries around your cases, then scope the capture to their PIDs, descendants and source record IDs before importing. The published selection is documented in `evidence/selection.json`; a full rerun capture may include additional background records.
