/* ==========================================================================
   Menumaker — Project Setup Screens
   Prototype interactions only. No app logic, no persistence.
   ========================================================================== */

(function () {
  'use strict';

  /* --- Generic date picker ------------------------------------------------
     Placeholder until a real picker lands. The field stays a text input so
     the mm/dd/yyyy display matches the comps; clicking the calendar button
     briefly swaps it to a native date input and opens the browser picker. */

  function openNativePicker(input) {
    var display = input.value;
    input.type = 'date';

    // mm/dd/yyyy -> yyyy-mm-dd for the native control.
    var parts = display.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (parts) {
      input.value = parts[3] + '-' + parts[1] + '-' + parts[2];
    }

    function restore() {
      var iso = input.value.match(/^(\d{4})-(\d{2})-(\d{2})$/);
      input.type = 'text';
      input.value = iso ? iso[2] + '/' + iso[3] + '/' + iso[1] : display;
      input.removeEventListener('change', restore);
      input.removeEventListener('blur', restore);
    }

    input.addEventListener('change', restore);
    input.addEventListener('blur', restore);

    if (typeof input.showPicker === 'function') {
      input.showPicker();
    } else {
      input.focus();
    }
  }

  document.addEventListener('click', function (event) {
    var trigger = event.target.closest('[data-date-trigger]');
    if (!trigger || trigger.disabled) return;

    var input = trigger.parentElement.querySelector('[data-date]');
    if (input && !input.disabled) openNativePicker(input);
  });

  /* --- Entity field: clear the selected record ---------------------------- */

  document.addEventListener('click', function (event) {
    var clear = event.target.closest('[data-clear-entity]');
    if (clear) clear.closest('.entity').remove();
  });

  /* --- Combo (multiselect / typeahead) ------------------------------------
     Clicking anywhere in the field surface focuses the text entry, so the
     whole control behaves like one input. */

  document.addEventListener('click', function (event) {
    var field = event.target.closest('.combo__field');
    if (!field || event.target.closest('button')) return;

    var input = field.querySelector('.combo__input');
    if (input) input.focus();
  });

  /* --- Dimensions preset list -------------------------------------------- */

  document.addEventListener('click', function (event) {
    var preset = event.target.closest('.preset');
    if (!preset) return;

    preset.closest('.preset-list')
      .querySelectorAll('.preset')
      .forEach(function (item) { item.classList.remove('is-active'); });

    preset.classList.add('is-active');
  });
}());
