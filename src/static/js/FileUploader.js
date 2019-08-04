(function(namespace) {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function noop(e) {
    e.stopPropagation();
    e.preventDefault();
  }

  function FileUploader($el, signUrl) {
    this.signUrl = signUrl;
    this.active = 0;

    this.$select = $el.getElementsByClassName('FileUploader--select')[0];
    this.$input = $el.getElementsByClassName('FileUploader--input')[0];
    this.$list = $el.getElementsByClassName('FileUploader--list')[0];

    this.$input.onchange = this.onChange.bind(this);
    this.$select.onclick = this.onSelect.bind(this);

    this.$select.addEventListener('dragenter', noop, false);
    this.$select.addEventListener('dragover', noop, false);
    this.$select.addEventListener('drag', this.onDrag.bind(this), false);

    this.upload = this.upload.bind(this);
  }

  FileUploader.prototype.allDone = function(e) {
    return this.active === 0
  };

  FileUploader.prototype.onDrag = function(e) {
    e.stopPropagation();
    e.preventDefault();

    const dt = e.dataTransfer;
    for(let i = 0; i < dt.files.length; i++) {
      this.upload(dt.files[i]);
    }
  };

  FileUploader.prototype.onSelect = function(e) {
    this.$input.click();
  };

  FileUploader.prototype.onChange = function () {
    for (let i = 0; i < this.$input.files.length; i++) {
      const file = this.$input.files[i];
      this.upload(file);
    }
  };

  FileUploader.prototype.upload = async function(file) {
    this.active++;
    try {
      const $status = this.uploadBegin(file);
      // sign request to upload file to s3
      let form = new FormData();
      form.append('filename', file.name);
      let response = await fetch(this.signUrl, {
        method: 'post',
        body: form,
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        }
      });
      const data = await response.json();

      // upload signed file to s3
      form = new FormData();
      for (let name in data.fields) {
        form.append(name, data.fields[name]);
      }
      form.append('file', file);
      await fetch(data.url, {
        method: 'POST',
        body: form,
      });

      this.uploadCompleted($status, data.fields.key);
    } finally {
      this.active--;
    }

    if (this.allDone()) {
      this.onUploadCompleted && this.onUploadCompleted();
    }
  };

  FileUploader.prototype.uploadBegin = function(file) {
    const $listItem = document.createElement('li');
    $listItem.setAttribute(
      'class',
      'list-group-item d-flex align-items-center FileUploader--listItem',
    );
    $listItem.style.height = '48px';

    const $status = document.createElement('div');
    $status.setAttribute('class', 'spinner-grow ml-auto');
    $status.setAttribute('aria-hidden', "true");
    $status.setAttribute('role', 'status');

    const $text = document.createElement('span');
    $text.setAttribute('class', 'sr-only');
    $status.appendChild($text);

    const $fileName = document.createElement('span');
    $fileName.innerText = file.name;
    $listItem.appendChild($fileName);
    $listItem.appendChild($status);

    const $cancelButton = this._cancelButton($listItem);
    $listItem.append($cancelButton);

    this.$list.appendChild($listItem);

    return $listItem;
  };

  FileUploader.prototype._cancelButton = function($parent) {
    const $cancelButton = document.createElement('button');
    $cancelButton.setAttribute('type', 'button');
    $cancelButton.setAttribute('class', 'ml-2 mb-1 close');
    $cancelButton.setAttribute('data-dismiss', 'toast');

    const $label = document.createElement('i');
    $label.setAttribute('class', 'fa fa-close');
    $cancelButton.append($label);
    $cancelButton.addEventListener('click', function () {
      this.$list.removeChild($parent);
    }.bind(this));

    return $cancelButton;
  };


  FileUploader.prototype.uploadCompleted = function($status, key) {
    if (!this.$list.contains($status)) {
      return;
    }
    $status.setAttribute('data-key', key);
    const spinners = $status.getElementsByClassName('spinner-grow');
    const button = $status.getElementsByTagName('button');
    $status.removeChild(spinners[0]);
    $status.removeChild(button[0]);
    let $ok = document.createElement('i');
    $ok.setAttribute('class', 'fa fa-check ml-auto mr-2');
    $status.appendChild($ok);
    const $cancelButton = this._cancelButton($status);
    $status.appendChild($cancelButton);
  };

  FileUploader.prototype.getUploadedFiles = function() {
    const files = [];
    const items = this.$list.getElementsByClassName('FileUploader--listItem');
    for (let i = 0; i < items.length; i++) {
      let key = items[i].getAttribute('data-key');
      if(key) {
        files.push(key)
      }
    }
    return files;
  };

  namespace.FileUploader = FileUploader;
})(window);
