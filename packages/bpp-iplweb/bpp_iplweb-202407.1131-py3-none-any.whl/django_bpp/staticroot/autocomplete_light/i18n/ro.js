/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(e){var n;(n=e&&e.fn&&e.fn.select2&&e.fn.select2.amd?e.fn.select2.amd:n).define("select2/i18n/ro",[],function(){return{errorLoading:function(){return"Rezultatele nu au putut fi incărcate."},inputTooLong:function(e){var n=e.input.length-e.maximum,e="Vă rugăm să ștergeți"+n+" caracter";return 1!=n&&(e+="e"),e},inputTooShort:function(e){return"Vă rugăm să introduceți "+(e.minimum-e.input.length)+" sau mai multe caractere"},loadingMore:function(){return"Se încarcă mai multe rezultate…"},maximumSelected:function(e){var n="Aveți voie să selectați cel mult "+e.maximum;return n+=" element",1!==e.maximum&&(n+="e"),n},noResults:function(){return"Nu au fost găsite rezultate"},searching:function(){return"Căutare…"},removeAllItems:function(){return"Eliminați toate elementele"}}}),n.define,n.require},event=new CustomEvent("dal-language-loaded",{lang:"ro"});document.dispatchEvent(event);