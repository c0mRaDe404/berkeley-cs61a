(define (duplicate lst)
  (cond
    ((null? lst) 
     nil)
    (else 
     (cons (car lst) (cons (car lst) (duplicate (cdr lst)))))
    )
)



(define (insert element lst index)
  (cond
    ((< index 0) (begin (print 'negative_index_no_no) nil))
    ((and (null? lst) (> index 0)) (begin (print 'out_of_bounds) nil))
    ((zero? index) (cons element lst))
    (else (cons (car lst) (insert element (cdr lst) (- index 1)))) 
  )
)
