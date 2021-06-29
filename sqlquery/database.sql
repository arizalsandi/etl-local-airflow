select  DISTINCT r.reviewid,
		r.artist,
		r.title,
		g.genre,
        l.label,
        y.year,
        c.content
from reviews as r
join genres as g ON g.reviewid = r.reviewid
join labels as l ON l.reviewid = r.reviewid
join years as y ON y.reviewid = r.reviewid
join content as c ON c.reviewid = r.reviewid