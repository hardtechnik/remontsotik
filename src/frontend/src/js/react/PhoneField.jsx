import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

import useDebounce from './useDebounce.jsx';


function PhoneField(props) {
  const [value, setValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const debouncedValue = useDebounce(value, 500);

  const startSearch = () => setIsSearching(true);
  const endSearch = () => {
    setIsSearching(false);
    setSuggestions([]);
  };
  const fetchPhoneModels = (device) => {
    fetch(`/phone/?name=${device}`, {
      method: 'get',
    }).then((response) => response.json()).then((data) => setSuggestions(data));
  };

  useEffect(() => {
    if (debouncedValue && isSearching) {
      fetchPhoneModels(debouncedValue);
    } else {
      setSuggestions([]);
    }
  }, [debouncedValue]);

  return (
    <div className="form-group">
      <label htmlFor="phone-model">Модель телефона:</label>
      <input
        type="text"
        className="form-control"
        id="phone-model"
        name="phone_model"
        aria-describedby="phone-model-help"
        placeholder="Введите модель телефона"
        value={value}
        onChange={({ target }) => setValue(target.value)}
        onKeyDown={startSearch}
        onBlur={endSearch}
      />
      <div className="autocomplete">
        {suggestions.length > 0 && (
          <ul className="autocomplete-list">
            {suggestions.map(({ DeviceName }) => (
              <li
                className="autocomplete-list-item"
                key={DeviceName}
                onMouseDown={(e) => {
                  setValue(e.currentTarget.innerText);
                  endSearch();
                }}
              >
                {DeviceName}
              </li>
            ))}
          </ul>
        )}
      </div>
      <small id="phone-model-help" className="form-text text-muted">
        Например, iphone x
      </small>
    </div>
  );
}

ReactDOM.render(<PhoneField />, document.getElementById("phone"));
