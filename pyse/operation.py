#!/usr/bin/env python
#coding=utf-8


def switch_page(driver):
    #print (driver.current_window_handle)
    handles = driver.window_handles
    #print (handles)
    for handle in handles:
        if handle!=driver.current_window_handle:
            #print ('switch to ',handle)
            driver.switch_to_window(handle)
            #print (driver.current_window_handle)
    #print(driver.title)

