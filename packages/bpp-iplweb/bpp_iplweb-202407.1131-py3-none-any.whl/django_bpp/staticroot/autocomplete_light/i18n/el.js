/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/el",[],function(){return{errorLoading:function(){return"Τα αποτελέσματα δεν μπόρεσαν να φορτώσουν."},inputTooLong:function(n){var e=n.input.length-n.maximum,n="Παρακαλώ διαγράψτε "+e+" χαρακτήρ";return 1==e&&(n+="α"),1!=e&&(n+="ες"),n},inputTooShort:function(n){return"Παρακαλώ συμπληρώστε "+(n.minimum-n.input.length)+" ή περισσότερους χαρακτήρες"},loadingMore:function(){return"Φόρτωση περισσότερων αποτελεσμάτων…"},maximumSelected:function(n){var e="Μπορείτε να επιλέξετε μόνο "+n.maximum+" επιλογ";return 1==n.maximum&&(e+="ή"),1!=n.maximum&&(e+="ές"),e},noResults:function(){return"Δεν βρέθηκαν αποτελέσματα"},searching:function(){return"Αναζήτηση…"},removeAllItems:function(){return"Καταργήστε όλα τα στοιχεία"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"el"});document.dispatchEvent(event);