import './styles/main.scss';
import { library, dom, icon } from '@fortawesome/fontawesome-svg-core';
import { faTimes } from '@fortawesome/free-solid-svg-icons'

library.add(faTimes);

document.addEventListener('DOMContentLoaded', () => {
  dom.i2svg();
});
