(function (namespace) {
  const $spinner = document.createElement('span');
  $spinner.setAttribute('class', 'spinner-border spinner-border-sm');

  function TicketForm($form, uploader) {
    this.$form = $form;
    this.$submit = document.getElementById('submit');
    this.uploader = uploader;
    this.initialize();
  }

  TicketForm.prototype.initialize = function() {
    this.uploader.onUploadCompleted = this.onUploadCompleted.bind(this);
    this.$form.addEventListener('submit', this.onSubmit.bind(this));
    this.$submit.addEventListener('click', this.onSubmitClicked.bind(this));
  };

  TicketForm.prototype.onSubmit = function() {
    const images = this.uploader.getUploadedFiles();
    const $images = document.getElementById('images');
    for(let i = 0; i < images.length; i++) {
      let $option = document.createElement('option');
      $option.setAttribute('value', images[i]);
      $option.setAttribute('selected', 'true');
      $images.appendChild($option);
    }
  };

  TicketForm.prototype.onUploadCompleted = function() {
    if(this.$submit.contains($spinner)) {
      this.$submit.removeChild($spinner);
      this.$submit.removeAttribute('disabled');
      this.$submit.click();
    }
  };

  TicketForm.prototype.onSubmitClicked = function(e) {
    if (!this.uploader.allDone()) {
      this.$submit.setAttribute('disabled', 'true');
      this.$submit.appendChild($spinner);
      e.stopPropagation();
      e.preventDefault();
    }
  };

  window.TicketForm = TicketForm;
})(window);
