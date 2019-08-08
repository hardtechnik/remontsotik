import FileUploader from './FileUploader';
import TicketForm from './TicketForm';

function init() {
  const signUrl = "/sign-file/";
  document.addEventListener("DOMContentLoaded", function() {
    const uploader = new FileUploader(
      document.getElementsByClassName('FileUploader')[0],
      signUrl,
    );
    new TicketForm(document.getElementById('ticket-form'), uploader);
  });
}

init();
