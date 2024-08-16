(ns client 
  (:require [necessary-evil.core :as xml-rpc]))

(defn main [opts]
  (println (xml-rpc/call "http://localhost:8000" :eval_code "bpy.data.objects.keys()")))