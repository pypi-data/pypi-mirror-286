/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var e;(e=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:e).define("select2/i18n/fi",[],function(){return{errorLoading:function(){return"Tuloksia ei saatu ladattua."},inputTooLong:function(n){return"Ole hyvä ja anna "+(n.input.length-n.maximum)+" merkkiä vähemmän"},inputTooShort:function(n){return"Ole hyvä ja anna "+(n.minimum-n.input.length)+" merkkiä lisää"},loadingMore:function(){return"Ladataan lisää tuloksia…"},maximumSelected:function(n){return"Voit valita ainoastaan "+n.maximum+" kpl"},noResults:function(){return"Ei tuloksia"},searching:function(){return"Haetaan…"},removeAllItems:function(){return"Poista kaikki kohteet"}}}),e.define,e.require},event=new CustomEvent("dal-language-loaded",{lang:"fi"});document.dispatchEvent(event);