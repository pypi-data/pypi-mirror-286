/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(e){var n;(n=e&&e.fn&&e.fn.select2&&e.fn.select2.amd?e.fn.select2.amd:n).define("select2/i18n/af",[],function(){return{errorLoading:function(){return"Die resultate kon nie gelaai word nie."},inputTooLong:function(e){var n=e.input.length-e.maximum,e="Verwyders asseblief "+n+" character";return 1!=n&&(e+="s"),e},inputTooShort:function(e){return"Voer asseblief "+(e.minimum-e.input.length)+" of meer karakters"},loadingMore:function(){return"Meer resultate word gelaai…"},maximumSelected:function(e){var n="Kies asseblief net "+e.maximum+" item";return 1!=e.maximum&&(n+="s"),n},noResults:function(){return"Geen resultate gevind"},searching:function(){return"Besig…"},removeAllItems:function(){return"Verwyder alle items"}}}),n.define,n.require},event=new CustomEvent("dal-language-loaded",{lang:"af"});document.dispatchEvent(event);