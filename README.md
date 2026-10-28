# Phishing to Endpoint Investigation

Tracing a controlled phishing delivery from the received email to Windows execution. The lab preserves the original EML messages, the delivered archive, its downloaded hash, native endpoint events and the related Splunk results.

The investigation starts with an urgent document-review request and a disguised command-script attachment. It follows the message and file into the endpoint records to establish what actually executed.

![Email deliveries in Splunk](images/01-message-deliveries-search.jpg)

## The case

An employee-benefits message asks for a document review before the end of the day. The same ZIP is attached and linked through the lab's internal HTTP service. Inside the archive, `Benefits-Review.pdf.cmd` is a command script whose name resembles a PDF.

Two SMTP deliveries were recorded. Execution was reproduced on **one endpoint**, `MOHAMEDAHMED`, using a safe payload that writes a local marker and makes an internal HTTP request. Delivery to the other mailbox is not evidence of execution there.

![Received message headers on Windows](images/windows-message-inspection.jpg)

## Evidence chain

1. Preserve the original message bytes and Message-ID.
2. Extract and hash the archive from the received message.
3. Download the linked archive and compare the hash: `96df2ee248bcf001c06821f51341a3760da79ead873a609b0def34f1266550de`.
4. Inspect the real file extension, then trace `cmd.exe` to its PowerShell child.
5. Correlate the marker file and internal HTTP connection with the executing PID `2052`.

![Extracted attachment files in Windows](images/windows-attachment-inspection.jpg)

Windows shows the complete `.pdf.cmd` extension. File properties identify it as a Windows Command Script.

![Actual attachment type](images/windows-attachment-properties.jpg)

![Process chain in Splunk](images/02-process-chain-search.jpg)

The saved marker records PowerShell PID 2052, matching the endpoint events.

![Saved result inspected in Notepad](images/windows-output-inspection.jpg)

## Investigation outcome

The attachment's command launcher started PowerShell, which wrote `review-result.json` with the computer, account, UTC time and PID. It also requested the internal `/phishing/ack?case=benefits-review` URL. Process, file and network records connect the activity to PowerShell PID 2052.

**The simulated phishing payload executed on one endpoint.** The two recorded deliveries identify the mailboxes to review; execution is established separately by the Windows evidence. The payload's result file is a local execution marker.

For incident triage, the relevant handoff is the received message, attachment hash, affected endpoint and account, process chain and connection. Other recipients and devices would then be checked for the same indicators. These are response recommendations; the lab's recorded outcome is delivery and controlled endpoint execution.

## Files

- [Investigation report](docs/investigation.md)
- [Search guide](docs/search-guide.md)
- [Build and reproduce](docs/reproduce.md)
- [Evidence index](evidence/README.md)
- [Original received email](evidence/mail/message-001.eml)
- [Delivered archive](evidence/Benefits-Review.zip)
- [Splunk process-chain export](evidence/search-results/02-process-chain.csv)

This is a local SMTP and Windows lab. It uses reserved example domains and a harmless payload; there is no credential collection, real malware or external command-and-control service.
