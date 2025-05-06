script/new-composer.sh  "Olivier Eugène Prosper Charles"  "Messiaen"  "Olivier Messiaen" 1908  1992  messiaen_o

script/new-piece.sh --title  "Quatuor pour la fin du temps"  --composer-code messiaen_o  --instruments  "String quartet"

script/new-collection.sh --title  "Organ works "  --editor  "Durand Paris"    --volume  "1"    --composer-code  "messiaen_o"    --instruments  "Organ"

script/new-piece.sh --title  "La Nativité du Seigneur"  --composer-code messiaen_o  --instruments  "Organ"

script/delete-piece.sh 2412e956aaa559a1b943f430a36363352d33bd47

script/delete-collection.sh ca652007c8b4177428c181785ea710d9

script/delete-composer.sh --code messiaen_o