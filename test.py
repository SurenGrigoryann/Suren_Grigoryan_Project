def open_portal(self,portal_opener,p1,p2):
        if ((self.y2 != self.rect.y) and 
        (((p1.rect.x <= portal_opener.rect.x + 15 and p1.rect.x >= portal_opener.rect.x - 15) and (p1.rect.y <= portal_opener.rect.y + 15 and p1.rect.y >= portal_opener.rect.y - 15))
        or
        ((p2.rect.x <= portal_opener.rect.x + 15 and p2.rect.x >= portal_opener.rect.x - 15) and (p2.rect.y <= portal_opener.rect.y + 15 and p2.rect.y >= portal_opener.rect.y - 15)))):
            
            self.rect.y += 1.25

        elif  (self.y1 != self.rect.y):
              
            self.rect.y -= 1.25