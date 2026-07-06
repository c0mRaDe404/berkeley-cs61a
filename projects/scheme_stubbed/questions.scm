(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement

(define (zip pairs)
  'replace-this-line)


;; Problem 5
;; Returns a list of two-element lists



(define (enumerate s)
  (define (helper counter lst)
    (cond
      ((null? lst)
       ())
      (else
       (cons
        (cons counter
              (cons (car lst) nil))
        (helper (+ counter 1)
                (cdr lst))))))

  (helper 0 s))



; BEGIN PROBLEM 5
; END PROBLEM 5

;; Problem 6

;; Merge two lists LIST1 and LIST2 according to COMP and return
;; the merged lists.
(define (merge comp list1 list2)
  ; BEGIN PROBLEM 6
  (cond ((null? list1) list2)
        ((null? list2) list1)
        ((comp (car list1) (car list2)) (cons (car list1) (merge comp (cdr list1) list2))) 
        ((comp (car list2) (car list1)) (cons (car list2) (merge comp list1 (cdr list2)))) 
  ) 
)
  ; END PROBLEM 6


(merge < '(1 5 7 9) '(4 8 10))
; expect (1 4 5 7 8 9 10)
(merge > '(9 7 5 1) '(10 8 4 3))
; expect (10 9 8 7 5 4 3 1)

;; Problem 7

(define (compare_two op lst)
    (op (car lst) (car (cdr lst)))
)

(define (slice lst index)
    (cond ((zero? index) lst)
          (else (slice (cdr lst) (- index 1)))))

(define non 
        (lambda (lst)
          (cond 
            ((null? lst) lst)
            ((< (length lst) 2) lst)
            ((compare_two <= lst)  (cons (car lst) (non (cdr lst))) )
            (else (cons (car lst) nil))
            )
))


(define (non_list s)
    ; BEGIN PROBLEM 17
   (cond ((null? s) s)
         ((< (length s) 2) cons(s nil))
          
         (else (define lst (non s)) 
               (cons lst (non_list (slice s (length lst))))
         )
         )    
)
    ; END PROBLEM 17

;; Problem EC
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM EC
         'replace-this-line
         ; END PROBLEM EC
         )
        ((quoted? expr)
         ; BEGIN PROBLEM EC
         'replace-this-line
         ; END PROBLEM EC
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM EC
           'replace-this-line
           ; END PROBLEM EC
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM EC
           'replace-this-line
           ; END PROBLEM EC
           ))
        (else
         ; BEGIN PROBLEM EC
         'replace-this-line
         ; END PROBLEM EC
         )))

