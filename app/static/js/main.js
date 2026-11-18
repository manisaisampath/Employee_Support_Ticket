/**
 * Employee Support Ticket System — main.js
 * Phase 10: Lightweight client-side enhancements.
 * Does NOT replace server-side validation.
 */

(function () {
  'use strict';

  /* ------------------------------------------------------------------
     1. Flash Message Auto-Dismiss
     Adds a close button to each alert and allows manual dismissal.
     Auto-dismiss success messages after 6 seconds.
  ------------------------------------------------------------------ */
  function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alert) {
      // Add dismiss button
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'alert-dismiss';
      btn.setAttribute('aria-label', 'Dismiss notification');
      btn.innerHTML = '&times;';
      btn.addEventListener('click', function () {
        dismissAlert(alert);
      });
      alert.appendChild(btn);

      // Auto-dismiss success messages after 6 seconds
      if (alert.classList.contains('alert-success')) {
        setTimeout(function () {
          dismissAlert(alert);
        }, 6000);
      }
    });
  }

  function dismissAlert(alert) {
    alert.style.transition = 'opacity 0.3s ease, max-height 0.3s ease, margin 0.3s ease, padding 0.3s ease';
    alert.style.opacity = '0';
    alert.style.maxHeight = '0';
    alert.style.marginBottom = '0';
    alert.style.paddingTop = '0';
    alert.style.paddingBottom = '0';
    alert.style.overflow = 'hidden';
    setTimeout(function () {
      if (alert.parentNode) {
        alert.parentNode.removeChild(alert);
      }
    }, 320);
  }

  /* ------------------------------------------------------------------
     2. Ticket Creation — Client-side validation hints
     Provides instant visual feedback; server validates authoritatively.
  ------------------------------------------------------------------ */
  function initTicketForm() {
    var form = document.getElementById('ticket-create-form');
    if (!form) return;

    var titleInput = form.querySelector('#title');
    var descInput  = form.querySelector('#description');

    // Live character counter for title
    if (titleInput) {
      var counter = document.createElement('span');
      counter.className = 'form-help';
      counter.id = 'title-char-count';
      titleInput.parentNode.appendChild(counter);

      function updateCounter() {
        var len = titleInput.value.length;
        var max = parseInt(titleInput.getAttribute('maxlength') || '100', 10);
        counter.textContent = len + ' / ' + max + ' characters';
        counter.style.color = len > max * 0.9 ? '#dc2626' : '';
      }
      titleInput.addEventListener('input', updateCounter);
      updateCounter();
    }

    // Warn on whitespace-only description blur
    if (descInput) {
      descInput.addEventListener('blur', function () {
        var existing = descInput.parentNode.querySelector('.form-error-text');
        if (existing) existing.remove();

        if (descInput.value.length > 0 && descInput.value.trim() === '') {
          var err = document.createElement('span');
          err.className = 'form-error-text';
          err.textContent = 'Description cannot be only whitespace.';
          descInput.parentNode.appendChild(err);
        }
      });
      descInput.addEventListener('input', function () {
        var existing = descInput.parentNode.querySelector('.form-error-text');
        if (existing) existing.remove();
      });
    }
  }

  /* ------------------------------------------------------------------
     3. Comment Form — Prevent empty submissions (client hint)
  ------------------------------------------------------------------ */
  function initCommentForms() {
    var forms = document.querySelectorAll('.comment-form form');
    forms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        var textarea = form.querySelector('textarea[name="content"]');
        if (textarea && textarea.value.trim() === '') {
          e.preventDefault();
          textarea.focus();
          var existing = form.querySelector('.form-error-text');
          if (!existing) {
            var err = document.createElement('span');
            err.className = 'form-error-text';
            err.textContent = 'Comment cannot be empty.';
            textarea.parentNode.appendChild(err);
          }
        }
      });
    });
  }

  /* ------------------------------------------------------------------
     4. Active nav link highlight
  ------------------------------------------------------------------ */
  function initNavHighlight() {
    var links = document.querySelectorAll('.nav-link');
    var current = window.location.pathname;
    links.forEach(function (link) {
      if (link.getAttribute('href') === current) {
        link.classList.add('nav-link-active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  /* ------------------------------------------------------------------
     Init
  ------------------------------------------------------------------ */
  document.addEventListener('DOMContentLoaded', function () {
    initFlashMessages();
    initTicketForm();
    initCommentForms();
    initNavHighlight();
  });

})();
