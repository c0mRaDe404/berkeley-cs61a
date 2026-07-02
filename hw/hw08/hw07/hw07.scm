(define (filter-lst fn lst) 
    (cond
      ((null? lst) nil)
      ((fn (car lst))
        (cons (car lst) (filter-lst fn (cdr lst)))
       )
      (else (filter-lst fn (cdr lst)))
      )   

  )

; ;; Tests
(define (even? x) (= (modulo x 2) 0))

(filter-lst even? '(0 1 1 2 3 5 8))

; expect (0 2 8)
(define (interleave first second) 
  (cond 
    ((null? first) second)
    ((null? second) first)
    (else (cons (car first) (cons (car second) (interleave (cdr first) (cdr second) )))))
  )

(interleave (list 1 3 5) (list 2 4 6))

; expect (1 2 3 4 5 6)
(interleave (list 1 3 5) nil)

; expect (1 3 5)
(interleave (list 1 3 5) (list 2 4))

; expect (1 2 3 4 5)
(define (accumulate combiner start n term)
 
  (cond 
    ((zero? n) start)
    (else (combiner (term n) (accumulate combiner start (- n 1) term)))
    )
    
  )

(define (check lst number)
  (cond ((null? lst) false)
        ((equal? (car lst) number) true)
        (else (check (cdr lst) number)) 
  )
 )

(define (no-repeats lst) 
   (cond 
     ((null? lst) nil)
     (else (if (check (cdr lst) (car lst))
              (no-repeats (cdr lst))
              (cons (car lst) (no-repeats (cdr lst)))
      ))
    ) 
)


