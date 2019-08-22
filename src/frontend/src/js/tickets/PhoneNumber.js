

export default class PhoneNumber {
  constructor($input, $error) {
    this.$input = $input;
    this.$error = $error;

    this.hasError = false;

    const onInput = this.onInput.bind(this);
    this.$input.addEventListener('change', this.validate.bind(this));
    this.$input.addEventListener('input', onInput);
    this.$input.addEventListener('paste', onInput);
  }

  setError(message) {
    this.$error.innerText = message;
    this.$input.classList.add('is-invalid');
    this.hasError = true;
  }

  cleanError() {
    if (this.hasError) {
      this.$input.classList.remove('is-invalid');
      this.hasError = false;
    }
  }

  onInput(e) {
    const value = this.$input.value;
    let result = value;

    this.cleanError();

    if(value.length > 10) {
        result = value.slice(0, 10);
    }

    const { inputType } = e;
    if (inputType === 'insertText') {
      if(!parseInt(e.data)) {
        result = value.slice(0, -1);
      }
    }

    if (isNaN(result) || !parseInt(result)) {
      result = '';
    }

    this.$input.value = result;
  }

  validate() {
    const value = this.$input.value;
    const length = value.length;
    if (length < 10) {
      this.setError('Слишком короткий номер телефона.');
    } else {
      this.cleanError();
    }
  }
}